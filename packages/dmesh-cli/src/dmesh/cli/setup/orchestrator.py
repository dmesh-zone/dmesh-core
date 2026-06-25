"""SetupOrchestrator for the dm setup command."""

import os
import sys
from pathlib import Path
from dmesh.cli.setup.config_writer import ConfigWriter, PROJECT_CONFIG_PATH
from dmesh.cli.setup.feedback import Feedback
from dmesh.sdk import AsyncSDK
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.config import get_settings


class SetupOrchestrator:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    async def run(self, flush: bool = False, rebuild: bool = False, topology: str = "docker-postgres") -> None:
        """Execute the initialisation sequence."""
        self._feedback.step("Initializing local data mesh environment...")
        
        if topology == "databricks-rest-pxy":
            missing = []
            for var in ["DATABRICKS_HOST", "DATABRICKS_CLIENT_ID", "DATABRICKS_CLIENT_SECRET", "DMESH_SDK__REST_PERSISTENCY_URL"]:
                if not os.getenv(var):
                    missing.append(var)
            if missing:
                raise ValueError(f"Missing required environment variables in .env for databricks-rest-pxy: {', '.join(missing)}")

        # Check if running in test mode (pytest)
        is_test = "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ
        
        use_rest_proxy = topology in (
            "docker-rest-pxy-postgres",
            "docker-rest-pxy-mem",
            "docker-rest-pxy-filesystem",
            "databricks-rest-pxy"
        )
        use_databricks_m2m = topology == "databricks-rest-pxy"
        api_in_memory = topology == "docker-rest-pxy-mem"
        api_filesystem = topology == "docker-rest-pxy-filesystem"
        
        if topology == "databricks-rest-pxy":
            rest_url = os.getenv('DMESH_SDK__REST_PERSISTENCY_URL') or os.getenv('DMESH_SDK__REST_PERSISTENCY_PROXY_URL')
            if not rest_url:
                raise ValueError("Missing DMESH_SDK__REST_PERSISTENCY_URL environment variable for databricks-rest-pxy topology")
        else:
            rest_url = "http://0.0.0.0:8000"

        cli_config_str = f"CLI SDK config:\n - rest_persistency_proxy: {use_rest_proxy}\n - rest_persistency_proxy_uses_databricks_m2m: {use_databricks_m2m}\n - rest_persistency_proxy_url: {rest_url}"
        
        if api_filesystem:
            db_type_str = "filesystem"
        else:
            db_type_str = 'memory' if api_in_memory else 'postgres'
            
        api_config_str = f"API Container config:\n - DMESH_SDK__IN_MEMORY_PERSISTENCY: {str(api_in_memory).lower()}\n - DMESH_SDK__FILESYSTEM_PERSISTENCY: {str(api_filesystem).lower()}\n - DB_TYPE: {db_type_str}"
        
        print("\n--- Setup Topology ---")
        print(cli_config_str)
        if topology not in ("databricks-rest-pxy", "filesystem"):
            print(api_config_str)

        if not is_test and topology != "filesystem":
            # Start infrastructure via docker-compose
            self._feedback.step("Starting infrastructure via docker-compose...")
            import subprocess
            try:
                cmd = ["docker-compose", "up", "-d"]
                if rebuild:
                    cmd.append("--build")
                
                env = os.environ.copy()
                env["DMESH_SDK__IN_MEMORY_PERSISTENCY"] = str(api_in_memory).lower()
                env["DMESH_SDK__FILESYSTEM_PERSISTENCY"] = str(api_filesystem).lower()
                env["DB_TYPE"] = db_type_str

                subprocess.run(cmd, check=True, capture_output=True, env=env)
                self._feedback.success("Infrastructure started.")
            except subprocess.CalledProcessError as e:
                self._feedback.error(f"Failed to start infrastructure: {e.stderr.decode()}")
                raise Exception("Docker Compose failed") from e

        # Ensure config directory exists
        PROJECT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        if not is_test:
            ConfigWriter(self._feedback).write_pg(
                host=os.getenv('DMESH_DB__HOST', 'localhost'),
                port=int(os.getenv('DMESH_DB__PORT', '5432')),
                user=os.getenv('DMESH_DB__USER', 'postgres'),
                password=os.getenv('DMESH_DB__PASSWORD', 'postgres'),
                dbname=os.getenv('DMESH_DB__NAME', 'postgres'),
                rest_persistency_proxy=use_rest_proxy,
                rest_persistency_proxy_uses_databricks_m2m=use_databricks_m2m,
                rest_persistency_proxy_url=rest_url,
                topology=topology,
                filesystem_persistency=(topology == "filesystem")
            )

        if is_test:
            # Use in-memory for unit tests
            self._feedback.step("Initializing in-memory repository for tests...")
            factory = RepositoryFactory().create(db_type="memory")
        else:
            if topology == "filesystem":
                self._feedback.step("Initializing filesystem repository...")
                settings = get_settings()
                root_dir = getattr(settings.sdk, "data_products_filesystem_root", None) or "tmp/data_products_filesystem_root"
                from dmesh.sdk.persistency.factory import FilesystemRepositoryFactory
                factory = FilesystemRepositoryFactory(root_dir)
            elif use_rest_proxy:
                self._feedback.step("Initializing REST Proxy repository...")
                from dmesh.sdk.persistency.rest import HttpRepositoryFactory
                # For local docker topologies that don't specify an env URL, we fallback to localhost for the CLI
                cli_api_url = f"{rest_url.rstrip('/')}/dmesh" if rest_url != "http://0.0.0.0:8000" else "http://localhost:8000/dmesh"
                factory = HttpRepositoryFactory(cli_api_url, use_m2m=use_databricks_m2m)
            else:
                self._feedback.step("Initializing Postgres database...")
                settings = get_settings()
                factory = RepositoryFactory().create(
                    db_type="postgres",
                    pg_host=settings.db.host,
                    pg_port=settings.db.port,
                    pg_user=settings.db.user,
                    pg_password=settings.db.password,
                    pg_db=settings.db.name
                )
        
        async with AsyncSDK(factory) as sdk:
            if flush:
                self._feedback.step("Flushing existing data...")
                await sdk.flush()
                self._feedback.success("Data flushed.")
        
        if is_test:
            mode = "test (in-memory)"
        else:
            mode = topology
            
        self._feedback.success(f"Data mesh initialised and ready ({mode} mode).")

        # ASCII architecture diagram
        print("\n--- Architecture Topology ---")
        if topology == "docker-postgres":
            print(" [CLI + SDK (rest proxy: false)] ---> [Postgres Container] ")
            print(" [API Container (db_type: postgres, memory: false)] ---> [Postgres Container] ")
        elif topology == "docker-rest-pxy-postgres":
            print(" [CLI + SDK (rest proxy: true)] ---> [API Container (db_type: postgres, memory: false)] ---> [Postgres Container] ")
        elif topology == "docker-rest-pxy-mem":
            print(" [CLI + SDK (rest proxy: true)] ---> [API Container (db_type: memory, memory: true)] ")
            print("                                      (Postgres Container is running but not used for persistency)")
        elif topology == "databricks-rest-pxy":
            print(" [CLI + SDK (rest proxy: true, m2m: true)] ---> [Databricks App] ")
        elif topology == "filesystem":
            print(" [CLI + SDK (filesystem persistency: true)] ---> [Local Filesystem] ")
        print("-----------------------------\n")

        # Invalidate cached settings so subsequent commands in the same REPL session reload the new config
        import dmesh.sdk.config
        dmesh.sdk.config._settings = None

        if topology not in ("databricks-rest-pxy", "filesystem"):
            print('Run "docker-compose logs -f api" to inspect api behavior\n')

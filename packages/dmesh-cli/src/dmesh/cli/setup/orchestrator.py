"""SetupOrchestrator for the dm setup command."""

import os
import sys
from pathlib import Path
from dmesh.cli.setup.config_writer import ConfigWriter, CONFIG_PATH
from dmesh.cli.setup.feedback import Feedback
from dmesh.sdk import AsyncSDK
from dmesh.sdk.persistency.factory import RepositoryFactory


class SetupOrchestrator:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    async def run(self, flush: bool = False, rebuild: bool = False, topology: str = "local-postgres-persistency") -> None:
        """Execute the initialisation sequence."""
        self._feedback.step("Initializing local data mesh environment...")
        
        # Check if running in test mode (pytest)
        is_test = "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ
        
        # Resolve shorthand topology
        if topology == "rest-pxy-local-postgres":
            topology = "local-rest-persistency-proxy-with-local-postgres-persistency"
        elif topology == "rest-pxy-local-mem":
            topology = "local-rest-persistency-proxy-with-local-in-memory-persistency"

        use_rest_proxy = topology in (
            "local-rest-persistency-proxy-with-local-postgres-persistency",
            "local-rest-persistency-proxy-with-local-in-memory-persistency"
        )
        api_in_memory = topology == "local-rest-persistency-proxy-with-local-in-memory-persistency"

        cli_config_str = f"CLI SDK config:\n - rest_persistency_proxy: {use_rest_proxy}\n - rest_persistency_proxy_url: http://0.0.0.0:8000"
        api_config_str = f"API Container config:\n - DMESH_SDK__IN_MEMORY_PERSISTENCY: {str(api_in_memory).lower()}\n - DB_TYPE: {'memory' if api_in_memory else 'postgres'}"
        
        print("\n--- Setup Topology ---")
        print(cli_config_str)
        print(api_config_str)

        if not is_test:
            # Start infrastructure via docker-compose
            self._feedback.step("Starting infrastructure via docker-compose...")
            import subprocess
            try:
                cmd = ["docker-compose", "up", "-d"]
                if rebuild:
                    cmd.append("--build")
                
                env = os.environ.copy()
                env["DMESH_SDK__IN_MEMORY_PERSISTENCY"] = str(api_in_memory).lower()
                env["DB_TYPE"] = "memory" if api_in_memory else "postgres"

                subprocess.run(cmd, check=True, capture_output=True, env=env)
                self._feedback.success("Infrastructure started.")
            except subprocess.CalledProcessError as e:
                self._feedback.error(f"Failed to start infrastructure: {e.stderr.decode()}")
                raise Exception("Docker Compose failed") from e

        # Ensure config directory exists
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        if not is_test:
            ConfigWriter(self._feedback).write_pg(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', '5432')),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres'),
                dbname=os.getenv('DB_NAME', 'postgres'),
                rest_persistency_proxy=use_rest_proxy
            )

        if is_test:
            # Use in-memory for unit tests
            self._feedback.step("Initializing in-memory repository for tests...")
            factory = RepositoryFactory().create(db_type="memory")
        else:
            if use_rest_proxy:
                self._feedback.step("Initializing REST Proxy repository...")
                from dmesh.sdk.persistency.rest import HttpRepositoryFactory
                factory = HttpRepositoryFactory("http://localhost:8000/dmesh")
            else:
                self._feedback.step("Initializing Postgres database...")
                factory = RepositoryFactory().create(
                    db_type="postgres",
                    pg_host=os.getenv('DB_HOST', 'localhost'),
                    pg_port=int(os.getenv('DB_PORT', '5432')),
                    pg_user=os.getenv('DB_USER', 'postgres'),
                    pg_password=os.getenv('DB_PASSWORD', 'postgres'),
                    pg_db=os.getenv('DB_NAME', 'postgres')
                )
        
        async with AsyncSDK(factory) as sdk:
            if flush:
                self._feedback.step("Flushing existing data...")
                await sdk.flush()
                self._feedback.success("Data flushed.")
        
        if is_test:
            mode = "test (in-memory)"
        elif topology == "local-rest-persistency-proxy-with-local-in-memory-persistency":
            mode = "In-Memory API"
        elif use_rest_proxy:
            mode = "Postgres API"
        else:
            mode = "Postgres"
            
        self._feedback.success(f"Data mesh initialised and ready ({mode} mode).")

        # ASCII architecture diagram
        print("\n--- Architecture Topology ---")
        if topology == "local-postgres-persistency":
            print(" [CLI + SDK (rest proxy: false)] ---> [Postgres Container] ")
            print(" [API Container (db_type: postgres, memory: false)] ---> [Postgres Container] ")
        elif topology == "local-rest-persistency-proxy-with-local-postgres-persistency":
            print(" [CLI + SDK (rest proxy: true)] ---> [API Container (db_type: postgres, memory: false)] ---> [Postgres Container] ")
        elif topology == "local-rest-persistency-proxy-with-local-in-memory-persistency":
            print(" [CLI + SDK (rest proxy: true)] ---> [API Container (db_type: memory, memory: true)] ")
            print("                                      (Postgres Container is running but not used for persistency)")
        print("-----------------------------\n")

        # Invalidate cached settings so subsequent commands in the same REPL session reload the new config
        import dmesh.sdk.config
        dmesh.sdk.config._settings = None

        print('Run "docker-compose logs -f api" to inspect api behavior\n')

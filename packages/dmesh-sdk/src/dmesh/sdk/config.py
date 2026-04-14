from __future__ import annotations
import os
import sys
import tomllib
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Type

from pydantic import BaseModel, Field, ValidationError
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

# Deep merge for TOML config
def _deep_update(base_dict: Dict[str, Any], update_with: Dict[str, Any]):
    for key, value in update_with.items():
        if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
            _deep_update(base_dict[key], value)
        else:
            base_dict[key] = value

class TomlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A custom settings source that loads configuration from one or more TOML files.
    Loads 'config/base.toml' first, then 'config/{profile}.toml' as an override.
    """
    def __init__(self, settings_cls: Type[BaseSettings], profile: str = "development"):
        super().__init__(settings_cls)
        self.profile = profile

    def get_field_value(self, field: Any, field_name: str) -> Tuple[Any, str, bool]:
        # This is for granular mapping, but we use __call__ to return a dict
        return None, field_name, False

    def __call__(self) -> Dict[str, Any]:
        config = {}
        config_dir = Path("config")
        
        # 1. Load base.toml (lowest priority in this source)
        base_path = config_dir / "base.toml"
        if base_path.exists():
            try:
                with base_path.open("rb") as f:
                    _deep_update(config, tomllib.load(f))
            except Exception as e:
                print(f"Error loading base config: {e}")
        
        # 2. Load profile-specific toml (e.g. development.toml, lakebase.toml)
        profile_path = config_dir / f"{self.profile}.toml"
        if profile_path.exists():
            try:
                with profile_path.open("rb") as f:
                    _deep_update(config, tomllib.load(f))
            except Exception as e:
                print(f"Error loading profile config '{self.profile}': {e}")
        
        return config

class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = Field(..., min_length=1) # Required secret
    name: str = "postgres"

class ApiSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

class SdkSettings(BaseModel):
    single_data_contract_per_product: bool = True
    dua_start_date_default: str = "2026-01-01"
    dua_purpose_default: str = "Unknown purpose"
    data_product_status_default: str = "active"
    data_contract_status_default: str = "active"
    expand_port_adapters: bool = True
    enrich_output_ports: bool = True

class Settings(BaseSettings):
    # Field names match the nesting in TOML and env vars
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    sdk: SdkSettings = Field(default_factory=SdkSettings)
    
    @property
    def profile(self) -> str:
        return os.getenv("APP_ENV", "development")

    model_config = SettingsConfigDict(
        env_prefix="DMESH_",
        env_nested_delimiter="__",
        # .env files order defined in get_settings to handle dynamic APP_ENV
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        profile = os.getenv("APP_ENV", "development")
        return (
            init_settings,      # 1. CLI flags / runtime args (highest priority)
            env_settings,       # 2. Environment variables
            dotenv_settings,    # 3 & 4. .env.{profile} and .env files
            TomlConfigSettingsSource(settings_cls, profile=profile), # 5 & 6. config/{profile}.toml and config/base.toml
            # Code defaults (last / lowest priority, implicitly handled by Pydantic)
        )

_settings: Optional[Settings] = None

def get_settings(**kwargs) -> Settings:
    """
    Initializes and returns the global settings instance.
    The profile is chosen via APP_ENV environment variable (default: development).
    Uses the priority stack:
    1. CLI flags / runtime args (passed to get_settings)
    2. Environment variables (DMESH_ pref)
    3. .env.{APP_ENV}
    4. .env
    5. config/{APP_ENV}.toml
    6. config/base.toml
    7. Code defaults
    """
    global _settings
    if _settings is None or kwargs:
        profile = os.getenv("APP_ENV", "development")
        
        # We dynamicallly set env_file list to respect profile priority
        # Pydantic-settings: later files take precedence
        env_files = [".env", f".env.{profile}"]
        
        class RuntimeSettings(Settings):
            model_config = SettingsConfigDict(
                env_prefix="DMESH_",
                env_nested_delimiter="__",
                env_file=env_files,
                env_file_encoding="utf-8",
                extra="ignore",
            )
            
        try:
            settings_obj = RuntimeSettings(**kwargs)
            if not kwargs: # Only cache if it's the default global settings
                _settings = settings_obj
            return settings_obj
        except ValidationError as e:
            print(f"Invalid configuration:\n{e}")
            sys.exit(1)
            
    return _settings

if __name__ == "__main__":
    # Example usage / validation test
    print("Testing configuration loading...")
    settings = get_settings()
    print(f"Profile: {settings.profile}")
    print(f"DB Host: {settings.db.host}")

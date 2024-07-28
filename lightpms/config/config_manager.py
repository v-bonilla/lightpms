from enum import Enum

from dotenv import dotenv_values


class Environment(Enum):
    DEV = 1
    PROD = 2


class ConfigManager:
    """Manages configuration for the lightpms system."""

    DOTENV_DEV_FILENAME = ".env.dev"
    DOTENV_PROD_FILENAME = ".env"

    def __init__(self, env: Environment) -> None:
        self._env = env
        dotenv_filename = (
            self.DOTENV_PROD_FILENAME
            if env == Environment.PROD
            else self.DOTENV_DEV_FILENAME
        )
        self._config = dotenv_values(dotenv_filename, verbose=True)

    def get_env(self) -> Environment:
        """Returns running environment."""
        return self._env

    def _get_config_value(self, key: str) -> str:
        """Get configuration value handling missing values.

        Args:
            key (str): Configuration key.

        Raises:
            KeyError: if key not loaded or is None.

        Returns:
            str: Configuration value.
        """
        if key not in self._config or self._config[key] is None:
            raise KeyError(f"f{key} not in loaded configuration.")
        config_value: str = self._config[key]  # type: ignore
        return config_value

    def get_postgres_host(self) -> str:
        """Returns host for postgres."""
        return self._get_config_value("POSTGRES_HOST")

    def get_postgres_database(self) -> str:
        """Returns database for postgres."""
        return self._get_config_value("POSTGRES_DATABASE")

    def get_postgres_user(self) -> str:
        """Returns user for postgres."""
        return self._get_config_value("POSTGRES_USER")

    def get_postgres_password(self) -> str:
        """Returns password for postgres."""
        return self._get_config_value("POSTGRES_PASSWORD")

    def get_exchange_api_key(self) -> str:
        """Returns api key for exchange."""
        return self._get_config_value("EXCHANGE_API_KEY")

    def get_exchange_secret_key(self) -> str:
        """Returns secret key for exchange."""
        return self._get_config_value("EXCHANGE_SECRET")

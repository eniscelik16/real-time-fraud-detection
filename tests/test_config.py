from src.core.config import app_config, env_settings


def test_config_loads_correctly():
    assert app_config.project_name == "Real-Time Fraud Detection Platform"
    assert app_config.data.test_size == 0.2
    assert env_settings.POSTGRES_PORT == 5432
    assert "postgresql://" in env_settings.database_url
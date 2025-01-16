from django.apps import AppConfig
from clickhouse.client import ClickHouseClient


class ClickHouseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clickhouse"

    def ready(self):
        """
        Initialize the global ClickHouse logger when the app is ready.
        """
        from clickhouse import services

        services.clickhouse_logger = ClickHouseClient()

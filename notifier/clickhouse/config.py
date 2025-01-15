import os
import datetime
import clickhouse_connect


class ClickHouseClient:
    def __init__(self):
        self.host = os.environ.get("CLICKHOUSE_HOST", "db")
        self.port = int(os.environ.get("CLICKHOUSE_PORT", 8123))
        self.username = os.environ.get("CLICKHOUSE_USER", "default")
        self.password = os.environ.get("CLICKHOUSE_PASSWORD", "default")
        self.database = os.environ.get("CLICKHOUSE_DB", "default")
        self.table = "logs"

        self.client = clickhouse_connect.get_client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
        )

        self._ensure_table()

    def _ensure_table(self):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            timestamp DateTime DEFAULT now(),
            level String,
            message String
        )
        ENGINE = MergeTree()
        ORDER BY timestamp
        """
        self.client.command(create_table_query)

    def log(self, level: str, message: str) -> None:
        row = [
            (
                datetime.datetime.now(),
                level.upper(),
                message,
            )
        ]
        self.client.insert(
            table=self.table,
            data=row,
        )

    def info(self, message: str) -> None:
        self.log("INFO", message)

    def error(self, message: str) -> None:
        self.log("ERROR", message)

    def debug(self, message: str) -> None:
        self.log("DEBUG", message)

    def warning(self, message: str) -> None:
        self.log("WARNING", message)

import os
import datetime
import clickhouse_connect

class ClickHouseClient:
    def __init__(
        self,
        host: str = "clickhouse",
        port: int = 8123,
        username: str = "default",
        password: str = "",
        database: str = "default",
        table: str = "logs",
    ):
        self.host = os.getenv("CLICKHOUSE_HOST", host)
        self.port = int(os.getenv("CLICKHOUSE_PORT", port))
        self.username = os.getenv("CLICKHOUSE_USER", username)
        self.password = os.getenv("CLICKHOUSE_PASSWORD", password)
        self.database = os.getenv("CLICKHOUSE_DB", database)
        self.table = table

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

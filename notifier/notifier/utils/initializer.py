from clickhouse.config import ClickHouseClient


class AppInitializer:
    """
    Centralized application initializer.
    """
    def __init__(self):
        self.clickhouse_logger = None

    def initialize_clickhouse_logger(self):
        """
        Initializes the ClickHouse logger.
        """
        self.clickhouse_logger = ClickHouseClient()

    def get_logger(self):
        if not self.clickhouse_logger:
            raise Exception("ClickHouseLogger has not been initialized!")
        return self.clickhouse_logger


app_initializer = AppInitializer()
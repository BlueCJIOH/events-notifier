from celery import shared_task

from clickhouse.services import clickhouse_logger



@shared_task
def log_task_status(method_name: str, *args, **kwargs):
    """
    Dynamically call a method on the ClickHouse logger.
    """
    try:
        if clickhouse_logger is None:
            raise RuntimeError("ClickHouseClient is not initialized.")

        method = getattr(clickhouse_logger, method_name, None)
        if method is None:
            raise AttributeError(f"Method {method_name} does not exist on ClickHouseClient.")

        # Call the method with the provided arguments
        method(*args, **kwargs)
    except Exception as e:
        raise RuntimeError(f"Failed to log to ClickHouse: {e}")

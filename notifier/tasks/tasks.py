import pika
import json
from celery import shared_task

from notifier.logger import LOGGER


@shared_task
def publish_task_message(task_id: int, user_id: int, status: str) -> None:
    """
    Publish message about the created task to RabbitMQ.
    """
    try:
        connection_params = pika.ConnectionParameters(
            host="rabbitmq",
            port=5672,
        )
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        channel.queue_declare(queue="tasks_queue", durable=True)

        message = {
            "user_id": user_id,
            "task_id": task_id,
            "status": status,
        }

        body = json.dumps(message)

        channel.basic_publish(exchange="", routing_key="tasks_queue", body=body)

        connection.close()

        LOGGER.info(f"Published task message: {message}")
    except Exception as e:
        LOGGER.exception(f"Failed to publish task message {e}")

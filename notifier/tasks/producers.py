import pika
import json

def publish_task_message(task) -> None:
    """
    Publish message about the created task to RabbitMQ.
    """
    connection_params = pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='tasks_queue', durable=True)

    message = {
        'user_id': task.user_id,
        'task_id': task.id,
        'status': task.status,
    }

    # Convert dict to string (JSON)
    body = json.dumps(message)

    channel.basic_publish(
        exchange='',
        routing_key='tasks_queue',
        body=body
    )

    connection.close()

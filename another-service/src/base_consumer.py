import json
import time
from concurrent.futures.thread import ThreadPoolExecutor

import pika
from sqlalchemy.orm import Session
from db.config import SessionLocal
from db.models import Task, TaskStatus


def publish_status_update(task_id: int, new_status, user_id) -> None:
    try:
        connection_params = pika.ConnectionParameters(host="rabbitmq", port=5672)
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        channel.queue_declare(queue="task_status_updates", durable=True)
        message = {"task_id": task_id, "status": new_status.value, "user_id": user_id}
        body = json.dumps(message)

        channel.basic_publish(exchange="", routing_key="task_status_updates", body=body)

        connection.close()
        print(f"Published status update for task {task_id}, status={new_status}")
    except Exception as e:
        print(f"Failed to publish status update: {e}")


def process_task(task_id: int, session: Session) -> None:
    """
    Process a task by updating its status in the database.
    :param task_id: ID of the task to process.
    :param session: SQLAlchemy session object.
    """
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        print(f"Task with ID {task_id} does not exist.")
        return

    try:
        task.status = TaskStatus.IN_PROGRESS
        session.commit()
        print(f"Task {task_id} updated to IN_PROGRESS.")
        publish_status_update(task.id, task.status, task.user_id)

        time.sleep(5)

        task.status = TaskStatus.DONE
        session.commit()
        print(f"Task {task_id} updated to DONE.")

        publish_status_update(task.id, task.status, task.user_id)
    except Exception as e:
        session.rollback()
        print(f"Failed to process task {task_id}: {e}")


def handle_message(body):
    """
    Handle a single message from RabbitMQ.
    """
    session = SessionLocal()
    try:
        message = json.loads(body)
        task_id = message.get("task_id")
        if not task_id:
            raise ValueError("Task ID is missing in the message.")

        process_task(task_id, session)
    except Exception as e:
        print(f"Failed to process message: {e}")
    finally:
        session.close()


def start_worker():
    """
    Start the RabbitMQ worker to consume messages and process tasks.
    """
    connection_params = pika.ConnectionParameters(host="rabbitmq", port=5672)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue="tasks_queue", durable=True)

    executor = ThreadPoolExecutor(max_workers=5)  # Adjust max_workers as needed

    def callback(ch, method, properties, body):
        """
        Callback for processing RabbitMQ messages.
        """
        # Submit the message to the thread pool for processing
        executor.submit(handle_message, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="tasks_queue", on_message_callback=callback)
    print("Worker started. Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        start_worker()
    except KeyboardInterrupt:
        print("Worker stopped manually.")

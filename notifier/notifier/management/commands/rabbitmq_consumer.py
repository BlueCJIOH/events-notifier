import json
import pika
from django.core.management.base import BaseCommand

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Command(BaseCommand):
    help = "Consumes messages from 'task_status_updates' queue and notifies websockets"

    def handle(self, *args, **options):
        connection_params = pika.ConnectionParameters(host='rabbitmq', port=5672)
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        channel.queue_declare(queue='task_status_updates', durable=True)

        def callback(ch, method, properties, body):
            try:
                data = json.loads(body)
                task_id = data.get("task_id")
                new_status = data.get("status")
                user_id = data.get("user_id")

                if not task_id or not new_status or not user_id:
                    raise ValueError("Missing task_id or status, user_id in the message.")

                group_name = f"room_{user_id}"

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        "type": "task_status_update",
                        "task_id": task_id,
                        "status": new_status,
                    }
                )

                print(f"Processed message successfully for task_id={task_id}, status={new_status}")
                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                print(f"Failed to process message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue='task_status_updates', on_message_callback=callback)
        print("Started consumer for 'task_status_updates' queue...")
        channel.start_consuming()

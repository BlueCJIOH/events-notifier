import json
from celery import shared_task
from django.db import transaction

from tasks.models import Task


# @shared_task
# def process_task_message(body: str) -> None:
#     """
#     Process incoming task message from RabbitMQ.
#     """
#     data = json.loads(body)
#     task_id = data.get('task_id')
#
#     with transaction.atomic():
#         task = Task.objects.select_for_update().get(pk=task_id)
#         task.status = Task.Status.IN_PROGRESS
#         task.save()

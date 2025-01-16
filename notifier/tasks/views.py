from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.tasks import publish_task_message


class TaskViewSet(ModelViewSet):
    """
    ViewSet for managing tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: TaskSerializer):
        """
        Publish task message to RabbitMQ after task creation.
        """
        task = serializer.save(user=self.request.user)
        publish_task_message.delay(task.id, task.user_id, task.status)

    def get_queryset(self):
        """
        Return only tasks for the authenticated user.
        """
        return super().get_queryset().filter(user=self.request.user)

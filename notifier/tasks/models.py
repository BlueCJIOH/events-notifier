from django.db import models
from django.conf import settings

from tasks.enums import TaskStatus


class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, choices=TaskStatus.items(), default=TaskStatus.PENDING.value
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Task #{self.pk} - {self.title}"

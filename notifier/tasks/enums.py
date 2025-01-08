from notifier.base import BaseEnum


class TaskStatus(BaseEnum):
    """Custom Enum for Task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
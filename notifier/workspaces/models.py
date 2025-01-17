from django.db import models

from roles.models import Role
from users.models import User
from workspaces.enums import MembershipStatusEnum

class Workspace(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "workspaces"

    def __str__(self) -> str:
        return self.name


class WorkspaceMember(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspace_memberships')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='workspace_members')
    is_active = models.CharField(
        max_length=10,
        choices=MembershipStatusEnum.items(),
        default=MembershipStatusEnum.ACTIVE.value
    )

    class Meta:
        db_table = "workspace_members"
        unique_together = ('workspace', 'user')
        indexes = [
            models.Index(fields=['user', 'workspace'], name='user_workspace_idx')
        ]

    def __str__(self) -> str:
        return f"{self.user.email} in {self.workspace.name}"

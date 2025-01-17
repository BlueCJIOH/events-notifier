from django.db import models

from roles.models import Role


class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "permissions"

    def __str__(self) -> str:
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

    class Meta:
        db_table = "role_permissions"
        unique_together = ('role', 'permission')

    def __str__(self) -> str:
        return f"{self.role.name} - {self.permission.name}"
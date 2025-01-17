from rest_framework.permissions import BasePermission

from workspaces.models import WorkspaceMember


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        workspace_id = request.data.get("workspace") or view.kwargs.get("workspace")

        if not workspace_id:
            return False

        required_permission = None

        action = getattr(view, "action", None)
        if action:
            method = getattr(view, action, None)
            required_permission = getattr(method, "required_permission", None)

        if not required_permission:
            return WorkspaceMember.objects.filter(
                user=request.user, workspace_id=workspace_id
            ).exists()

        return WorkspaceMember.objects.filter(
            user=request.user,
            workspace_id=workspace_id,
            role__permissions__name=required_permission,
        ).exists()

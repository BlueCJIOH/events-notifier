from rest_framework.permissions import BasePermission

from workspaces.models import WorkspaceMember


class IsWorkspaceMember(BasePermission):
    def has_permission(self, request, view):
        workspace_id = request.data.get("workspace") or view.kwargs.get("workspace")

        if not workspace_id:
            return False

        return WorkspaceMember.objects.filter(
            workspace_id=workspace_id, user_id=request.user.id
        ).exists()

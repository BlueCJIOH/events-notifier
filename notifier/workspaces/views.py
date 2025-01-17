from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from config.base import require_permission
from permissions.permissions import RolePermission
from roles.models import Role
from workspaces.models import Workspace, WorkspaceMember
from workspaces.permissions import IsWorkspaceMember
from workspaces.serializers import WorkspaceSerializer, WorkspaceMemberSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        workspace = serializer.save()
        owner_role = Role.objects.get(name="Owner")  # Getting Owner role

        # Add the current user to the workspace as the owner
        WorkspaceMember.objects.create(
            workspace=workspace, user=self.request.user, role=owner_role, is_active=True
        )


class WorkspaceMemberViewSet(viewsets.ModelViewSet):
    queryset = WorkspaceMember.objects.all()
    serializer_class = WorkspaceMemberSerializer
    permission_classes = (IsAuthenticated, IsWorkspaceMember, RolePermission)

    @require_permission("workspacemember.add_member")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

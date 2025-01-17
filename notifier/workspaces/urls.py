from django.urls import path, include
from rest_framework.routers import DefaultRouter

from workspaces.views import WorkspaceViewSet, WorkspaceMemberViewSet

router = DefaultRouter()

router.register(r"workspace", WorkspaceViewSet, basename="workspace")
router.register(r"member", WorkspaceMemberViewSet, basename="workspace-member")

urlpatterns = [
    path("", include(router.urls)),
]

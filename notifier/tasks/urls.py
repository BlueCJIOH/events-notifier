from rest_framework.routers import DefaultRouter

from tasks.views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = router.urls

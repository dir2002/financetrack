from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, task_list, task_assign_multiple, task_unassign_multiple


router = DefaultRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path('tasks/', task_list, name='task_list'),
    path('tasks/assign/', task_assign_multiple, name='task_assign_multiple'), # type: ignore
    path('tasks/unassign/', task_unassign_multiple, name='task_unassign_multiple'), # type: ignore
]

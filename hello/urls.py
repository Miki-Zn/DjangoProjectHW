from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    greeting,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatsView,
    TaskByDayView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    SubTaskPaginatedListView,
    SubTaskFilterView,
    CategoryViewSet,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', greeting, name='greeting'),


    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('tasks/by-day/', TaskByDayView.as_view(), name='task-by-day'),


    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/paginated/', SubTaskPaginatedListView.as_view(), name='subtask-paginated'),
    path('subtasks/filter/', SubTaskFilterView.as_view(), name='subtask-filter'),
    path('subtasks/<int:id>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-retrieve-update-destroy'),


    path('', include(router.urls)),
]

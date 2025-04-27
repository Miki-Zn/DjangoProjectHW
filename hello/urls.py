from django.urls import path
from .views import (
    greeting,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatsView,
    TaskByDayView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', greeting, name='greeting'),

    # Task endpoints
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('tasks/by-day/', TaskByDayView.as_view(), name='tasks-by-day'),

    # SubTask endpoints
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-retrieve-update-destroy'),
]

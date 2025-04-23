from django.urls import path
from .views import (
    greeting,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path('', greeting, name='greeting'),


    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),


    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]

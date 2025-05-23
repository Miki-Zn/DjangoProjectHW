from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatsView,
    TaskByDayView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    CategoryViewSet,
)

from django.http import HttpResponse

def greeting(request):
    return HttpResponse("Hello, this is greeting view.")


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [

    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('tasks/by-day/', TaskByDayView.as_view(), name='task-by-day'),


    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-retrieve-update-destroy'),


    path('', include(router.urls)),


    path('', greeting, name='greeting'),
]

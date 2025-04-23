from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from django.http import HttpResponse
from django.db import models

from .models import Task, SubTask
from .serializers import (
    TaskSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    SubTaskCreateSerializer,
    SubTaskSerializer
)


def greeting(request):
    return HttpResponse("Привет!")


# ==== Task Views ====

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'id'


class TaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        status_counts = Task.objects.values('status').annotate(count=models.Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=now()).count()
        return Response({
            'total_tasks': total_tasks,
            'status_counts': status_counts,
            'overdue_tasks': overdue_tasks
        })



class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'id'

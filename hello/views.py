from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now
from django.http import HttpResponse
from django.db import models
import calendar

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


class TaskByDayView(APIView):
    def get(self, request):
        day_param = request.query_params.get('day')
        tasks = Task.objects.all()

        if day_param:
            try:
                day_index = list(calendar.day_name).index(day_param.capitalize())
                tasks = tasks.filter(deadline__week_day=(day_index + 2) % 7 or 7)
            except ValueError:
                return Response({"error": "Invalid day"}, status=400)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# ==== SubTask Views ====

class SubTaskPagination(PageNumberPagination):
    page_size = 5


class FilteredSubTaskView(ListAPIView):
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')
        task_name = self.request.query_params.get('task_name')
        status = self.request.query_params.get('status')

        if task_name:
            queryset = queryset.filter(task__title__icontains=task_name)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class SubTaskListView(ListAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination


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

class SubTaskPaginatedListView(ListAPIView):
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')
        task_name = self.request.query_params.get('task_name')
        status = self.request.query_params.get('status')

        if task_name:
            queryset = queryset.filter(task__title__icontains=task_name)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

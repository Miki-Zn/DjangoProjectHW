from rest_framework import generics, filters, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now
from django.http import HttpResponse
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
import calendar

from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    SubTaskCreateSerializer,
    SubTaskSerializer,
    CategorySerializer,
    CategoryDetailSerializer
)


def greeting(request):
    return HttpResponse("Hello!")


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
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
        day_param = request.query_params.get('day', '').strip()
        valid_days = [d.lower() for d in calendar.day_name]

        if day_param:
            day_lower = day_param.lower()
            if day_lower not in valid_days:
                return Response({"error": "Invalid day"}, status=status.HTTP_400_BAD_REQUEST)
            day_index = valid_days.index(day_lower)
            tasks = Task.objects.filter(deadline__week_day=(day_index + 2) % 7 or 7)
        else:
            tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'id'


class SubTaskPaginatedListView(generics.ListAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    pagination_class = StandardResultsSetPagination


class SubTaskFilterView(APIView):
    def get(self, request):
        queryset = SubTask.objects.all()
        task_name = request.query_params.get('task_name')
        status_param = request.query_params.get('status')

        if task_name:
            queryset = queryset.filter(task__title__icontains=task_name)
        if status_param:
            queryset = queryset.filter(status=status_param)

        serializer = SubTaskSerializer(queryset, many=True)
        return Response(serializer.data)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        tasks_count = category.task_set.count()
        return Response({'tasks_count': tasks_count})

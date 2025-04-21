from django.contrib import admin
from .models import Task, SubTask, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories', 'deadline')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

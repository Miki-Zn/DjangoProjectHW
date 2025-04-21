from django.contrib import admin
from .models import Task, SubTask, Category

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)


from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone


class SubTaskCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)
    deadline = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if Category.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        now = timezone.now().date()
        if value and value < now:
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(source='subtask_set', many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'categories']

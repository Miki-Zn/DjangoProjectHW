# Generated by Django 5.2 on 2025-04-24 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_alter_subtask_title_alter_task_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.AlterModelOptions(
            name='subtask',
            options={},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='category',
            name='unique_category_name',
        ),
        migrations.RemoveConstraint(
            model_name='subtask',
            name='unique_subtask_title',
        ),
        migrations.RemoveConstraint(
            model_name='task',
            name='unique_task_title',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.task'),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterModelTable(
            name='category',
            table=None,
        ),
        migrations.AlterModelTable(
            name='subtask',
            table=None,
        ),
        migrations.AlterModelTable(
            name='task',
            table=None,
        ),
    ]

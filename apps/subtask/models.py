from django.db import models

from apps.user.models import User
from apps.category.models import Category
from apps.status.models import Status
from apps.task.models import Task


class SubTask(models.Model):
    title = models.CharField(max_length=75, blank=True)
    description = models.CharField(max_length=1500, blank=True)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks',
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET(1),
        blank=True,
        null=True
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    date_started = models.DateField(blank=True)
    deadline = models.DateField(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title[:6]}..."

    def count_by_status(self, status_name):
        try:
            status = Status.objects.get(name=status_name)
        except Status.DoesNotExist:
            return 0

        count = SubTask.objects.filter(status=status).count()

        return count

    def count_by_category(self, category_name):
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return 0

        count = SubTask.objects.filter(category=category).count()

        return count

    class Meta:
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'

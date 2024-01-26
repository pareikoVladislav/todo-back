from django.db import models

from apps.user.models import User
from apps.category.models import Category
from apps.status.models import Status


class Task(models.Model):
    title = models.CharField(
        max_length=75,
        default="DEFAULT TITLE",
        unique_for_date='date_started'
    )
    description = models.TextField(
        max_length=1500,
        verbose_name="task details",
        default="Here you can add your description..."
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET(1),
        blank=True,
        null=True
    )
    date_started = models.DateField(
        help_text="День, когда задача должна начаться",
        blank=True,
        null=True
    )
    deadline = models.DateField(
        help_text="День, когда задача должна быть выполнена",
        blank=True,
        null=True
    )
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

        count = Task.objects.filter(status=status).count()

        return count

    def count_by_category(self, category_name):
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return 0

        count = Task.objects.filter(category=category).count()

        return count

    # @property
    # def count_subtasks(self):
    #     try:
    #         count = SubTask.objects.filter(
    #             task=self.id
    #         ).count()
    #     except SubTask.DoesNotExist:
    #         return 0
    #
    #     return count

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

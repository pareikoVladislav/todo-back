import datetime

from rest_framework import serializers

from apps.task.error_messages import (
    TITLE_LENGTH_ERROR_MESSAGE,
    DESCRIPTION_LENGTH_ERROR_MESSAGE,
    INCORRECT_DATE_STARTED_ERROR_MESSAGE,
    INCORRECT_DEADLINE_ERROR_MESSAGE,
    TITLE_REQUIRED_ERROR_MESSAGE,
)
from apps.task.models import Task
from apps.subtask.serializers import SubTaskPreviewSerializer


def validate_fields(attrs):
    title = attrs.get('title')
    description = attrs.get('description')
    date_started = attrs.get('date_started')
    deadline = attrs.get('deadline')

    if not title:
        raise serializers.ValidationError(
            TITLE_REQUIRED_ERROR_MESSAGE
        )

    if len(title) > 75:
        raise serializers.ValidationError(
            TITLE_LENGTH_ERROR_MESSAGE
        )
    if description and len(description) > 1499:
        raise serializers.ValidationError(
            DESCRIPTION_LENGTH_ERROR_MESSAGE
        )
    if date_started and date_started < datetime.date.today():
        raise serializers.ValidationError(
            INCORRECT_DATE_STARTED_ERROR_MESSAGE
        )
    if deadline and deadline < date_started:
        raise serializers.ValidationError(
            INCORRECT_DEADLINE_ERROR_MESSAGE
        )

    return attrs


class TaskInfoSerializer(serializers.ModelSerializer):
    subtasks = SubTaskPreviewSerializer(many=True, read_only=True)

    category = serializers.StringRelatedField()
    status = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'category',
            'status',
            'date_started',
            'deadline',
            'created_at',
            'subtasks'
        ]

    def validate(self, attrs):
        return validate_fields(attrs=attrs)


class AllTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'creator',
            'category',
            'status',
            'date_started',
            'deadline',
            'created_at'
        ]

    def validate(self, attrs):
        return validate_fields(attrs=attrs)

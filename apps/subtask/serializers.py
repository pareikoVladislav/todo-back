import datetime

from rest_framework import serializers

from apps.category.models import Category
from apps.status.models import Status
from apps.subtask.models import SubTask
from apps.user.models import User
from apps.subtask.error_messages import (
    TITLE_LENGTH_ERROR_MESSAGE,
    TITLE_REQUIRED_ERROR_MESSAGE,
    INCORRECT_DATE_STARTED_ERROR_MESSAGE,
    INCORRECT_DEADLINE_ERROR_MESSAGE,
    DESCRIPTION_LENGTH_ERROR_MESSAGE
)


def validate_fields(attrs):
    title = attrs.get('title')
    description = attrs.get('description')
    date_started = attrs.get('date_started')
    deadline = attrs.get('deadline')

    if title is None:
        raise serializers.ValidationError(
            TITLE_REQUIRED_ERROR_MESSAGE
        )

    if title and len(title) > 75:
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


class ListSubTasksSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Status.objects.all()
    )
    creator = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )

    class Meta:
        model = SubTask
        fields = [
            'id',
            'title',
            'description',
            'category',
            'task',
            'status',
            'creator',
            'date_started',
            'deadline',
            'created_at'
        ]

    def validate(self, attrs):
        return validate_fields(attrs=attrs)


class SubTaskInfoSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Status.objects.all()
    )

    creator = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )

    class Meta:
        model = SubTask
        fields = [
            'id',
            'title',
            'description',
            'category',
            'status',
            'creator',
            'date_started',
            'deadline'
        ]

    def validate(self, attrs):
        return validate_fields(attrs=attrs)


class SubTaskPreviewSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'status']

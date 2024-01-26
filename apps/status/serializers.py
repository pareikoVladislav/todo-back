from rest_framework import serializers

from apps.status.error_messages import (
    STATUS_NAME_LEN_ERROR_MESSAGE,
    NON_UNIQUE_STATUS_NAME_ERROR_MESSAGE
)
from apps.status.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def validate_name(self, value):
        if Status.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                NON_UNIQUE_STATUS_NAME_ERROR_MESSAGE
            )

        if len(value) < 3 or len(value) > 30:
            raise serializers.ValidationError(
                STATUS_NAME_LEN_ERROR_MESSAGE
            )

        return value

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.category.error_messages import (
    CATEGORY_NAME_LEN_ERROR_MESSAGE,
    NON_UNIQUE_CATEGORY_NAME_ERROR_MESSAGE,
)
from apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError(
                NON_UNIQUE_CATEGORY_NAME_ERROR_MESSAGE
            )

        if len(value) < 4 or len(value) > 25:
            raise ValidationError(
                CATEGORY_NAME_LEN_ERROR_MESSAGE
            )

        return value

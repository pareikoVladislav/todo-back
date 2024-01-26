from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.category.success_messages import (
    NEW_CATEGORY_CREATED_MESSAGE,
    CATEGORY_UPDATED_SUCCESSFULLY_MESSAGE,
    CATEGORY_WAS_DELETED_SUCCESSFUL,
)
from apps.category.models import Category
from apps.category.serializers import (
    CategorySerializer,
)


class CategoryListGenericView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request: Request, *args, **kwargs):
        categories = self.get_queryset()

        if categories:
            serializer = self.serializer_class(categories, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )

        else:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data=[]
            )

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    "message": NEW_CATEGORY_CREATED_MESSAGE,
                    "data": serializer.data
                }
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )


class RetrieveCategoryGenericView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_object(self):
        category_id = self.kwargs.get("category_id")

        category = get_object_or_404(Category, id=category_id)

        return category

    def get(self, request: Request, *args, **kwargs):
        category = self.get_object()

        serializer = self.serializer_class(category)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def put(self, request: Request, *args, **kwargs):
        category = self.get_object()

        serializer = self.serializer_class(category, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": CATEGORY_UPDATED_SUCCESSFULLY_MESSAGE,
                    "data": serializer.data
                }
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

    def delete(self, request, *args, **kwargs):
        category = self.get_object()

        category.delete()

        return Response(
            status=status.HTTP_200_OK,
            data=CATEGORY_WAS_DELETED_SUCCESSFUL
        )


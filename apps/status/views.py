from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from apps.status.success_messages import (
    NEW_STATUS_CREATED_MESSAGE,
    STATUS_UPDATED_SUCCESSFULLY_MESSAGE,
    STATUS_WAS_DELETED_SUCCESSFUL,
)
from apps.status.models import Status
from apps.status.serializers import (
    StatusSerializer,
)


class StatusListGenericView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

    def get(self, request: Request, *args, **kwargs):
        statuses = self.get_queryset()

        if statuses:
            serializer = self.serializer_class(statuses, many=True)

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
                    "message": NEW_STATUS_CREATED_MESSAGE,
                    "data": serializer.data
                }
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )


class RetrieveStatusGenericView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StatusSerializer

    def get_object(self):
        status_id = self.kwargs.get("status_id")

        status_obj = get_object_or_404(Status, id=status_id)

        return status_obj

    def get(self, request: Request, *args, **kwargs):
        status_obj = self.get_object()

        serializer = self.serializer_class(status_obj)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def put(self, request: Request, *args, **kwargs):
        status_obj = self.get_object()

        serializer = self.serializer_class(status_obj, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": STATUS_UPDATED_SUCCESSFULLY_MESSAGE,
                    "data": serializer.data
                }
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

    def delete(self, request, *args, **kwargs):
        status_obj = self.get_object()

        status_obj.delete()

        return Response(
            status=status.HTTP_200_OK,
            data=STATUS_WAS_DELETED_SUCCESSFUL
        )

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status


from apps.subtask.models import SubTask
from apps.subtask.serializers import (
    ListSubTasksSerializer,
    SubTaskInfoSerializer
)
from apps.subtask.success_messages import (
    SUBTASK_UPDATED_SUCCESSFULLY_MESSAGE,
    SUBTASK_WAS_DELETED_SUCCESSFUL,
    NEW_SUBTASK_CREATED_MESSAGE,
)


class SubTasksListGenericView(ListCreateAPIView):
    serializer_class = ListSubTasksSerializer

    def get_queryset(self):
        queryset = SubTask.objects.select_related(
            'category',
            'status'
        )

        status_obj = self.request.query_params.get("status")
        category = self.request.query_params.get("category")
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        deadline = self.request.query_params.get("deadline")

        if status_obj:
            queryset = queryset.filter(
                status__name=status_obj
            )
        if category:
            queryset = queryset.filter(
                category__name=category
            )
        if date_from and date_to:
            queryset = queryset.filter(
                date_started__range=[date_from, date_to]
            )
        if deadline:
            queryset = queryset.filter(
                deadline=deadline
            )

        return queryset

    def get(self, request: Request, *args, **kwargs):
        filtered_data = self.get_queryset()

        if filtered_data.exists():
            serializer = self.serializer_class(
                instance=filtered_data,
                many=True
            )

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data=[]
        )

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": NEW_SUBTASK_CREATED_MESSAGE,
                "data": serializer.data
            }
        )


class SubTaskDetailGenericView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubTaskInfoSerializer

    def get_object(self):
        subtask_id = self.kwargs.get("subtask_id")

        subtask = get_object_or_404(SubTask, id=subtask_id)

        return subtask

    def get(self, request: Request, *args, **kwargs):
        subtask = self.get_object()

        serializer = self.serializer_class(subtask)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def put(self, request: Request, *args, **kwargs):
        subtask = self.get_object()

        serializer = self.serializer_class(subtask, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": SUBTASK_UPDATED_SUCCESSFULLY_MESSAGE,
                    "data": serializer.data
                }
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

    def delete(self, request, *args, **kwargs):
        subtask = self.get_object()

        subtask.delete()

        return Response(
            status=status.HTTP_200_OK,
            data=SUBTASK_WAS_DELETED_SUCCESSFUL
        )

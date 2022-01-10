from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Note
from .serializers import NoteSerializer
from .tasks import add


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    @action(detail=False)
    def add_job_ulala(self, request):
        task = add.delay(
            1, 2
        )

        return Response({
            'task_id': task.id,
        })

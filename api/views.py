from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Note, Store
from .serializers import NoteSerializer, StoreSerializer
from .tasks import add


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    @action(detail=False)
    def add_job_ulala(self, request):
        task = add.delay(
            1, 2
        )

        store = Store.objects.first()

        return Response({
            'task_id': task.id,
        })


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @action(detail=True)
    def update_pricing(self, request, pk):
        store = self.get_object()
        products = store.update_pricing()

        print("STOREEEEEEEEEEEEEEEEEEEEEEEEE")
        print(store)
        print(products)

        return Response(products)

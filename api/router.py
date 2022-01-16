from rest_framework import routers

from api.views import NoteViewSet, StoreViewSet

router = routers.SimpleRouter()
router.register(r'notes', NoteViewSet)
router.register(r'stores', StoreViewSet)

from rest_framework import routers

from api.views import NoteViewSet

router = routers.SimpleRouter()
router.register(r'notes', NoteViewSet)

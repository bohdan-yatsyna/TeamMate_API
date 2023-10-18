from rest_framework.routers import DefaultRouter
from person.views import PersonViewSet

app_name = "persons"

router = DefaultRouter()
router.register("", PersonViewSet, basename="person")

urlpatterns = [] + router.urls

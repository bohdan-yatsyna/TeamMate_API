from rest_framework.routers import DefaultRouter

from team.views import TeamViewSet


app_name = "teams"

router = DefaultRouter()
router.register("", TeamViewSet, basename="team")

urlpatterns = [] + router.urls

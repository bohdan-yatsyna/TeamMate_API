from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from person.views import (
    AdminPersonViewSet,
    ManagePersonView,
    RegisterPersonView,
)


app_name = "persons"

router = DefaultRouter()
router.register("", AdminPersonViewSet)

urlpatterns = [
    path("register/", RegisterPersonView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair_and_login",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin_user/", include(router.urls), name="admin_only"),
    path("me/", ManagePersonView.as_view(), name="manage"),
]

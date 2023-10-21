from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from person.serializers import CreatePersonSerializer, ManagePersonSerializer


class RegisterPersonView(generics.CreateAPIView):
    serializer_class = CreatePersonSerializer
    permission_classes = (AllowAny,)


class ManagePersonView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ManagePersonSerializer

    def get_object(self):
        return self.request.user


class AdminPersonViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ManagePersonSerializer
    permission_classes = (IsAdminUser,)

    def check_permissions(self, request):
        super().check_permissions(request)

        if not request.user.is_superuser:
            self.permission_denied(
                request, message="Only admin users have access to this endpoint."
            )

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = get_user_model().objects.select_related("team")

        return queryset

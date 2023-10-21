from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from person.serializers import CreatePersonSerializer, ManagePersonSerializer


class RegisterPersonView(generics.CreateAPIView):
    """
    View for Person registering on the portal, Authentication is not required.
    """
    serializer_class = CreatePersonSerializer
    permission_classes = (AllowAny,)


# Only for documentation endpoint details
@extend_schema_view(
    get=extend_schema(
        description="Endpoint with detailed Person page for current user."
    ),
    put=extend_schema(
        description="Endpoint for updating current Person details by id."
    ),
    patch=extend_schema(
        description=(
            "Endpoint for partial updating current Person details by id."
        )
    ),
    delete=extend_schema(
        description="Endpoint for deleting current Person's account by id."
    )
)
class ManagePersonView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ManagePersonSerializer

    def get_object(self):
        return self.request.user


# Only for documentation endpoint details
@extend_schema_view(
    create=extend_schema(
        description=(
            "Endpoint for creating Person by Admin user."
        )
    ),
    retrieve=extend_schema(
        description=(
            "Endpoint with detailed Person's page by id for Admin users."
        )
    ),
    update=extend_schema(
        description=(
            "Endpoint for updating a specific "
            "Person's details by id for Admin users."
        )
    ),
    partial_update=extend_schema(
        description=(
            "Endpoint for partially updating a specific "
            "Person's details by id for Admin users."
        )
    ),
    destroy=extend_schema(
        description=(
            "Endpoint for deleting a specific Person by id for Admin users."
        )
    ),
    list=extend_schema(
        description="Endpoint for listing all Persons for Admin users."
    ),
)
class AdminPersonViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ManagePersonSerializer
    permission_classes = (IsAdminUser,)

    def check_permissions(self, request):
        super().check_permissions(request)

        if not request.user.is_superuser:
            self.permission_denied(
                request,
                message="Only admin users have access to this endpoint.",
            )

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = get_user_model().objects.select_related("team")

        return queryset

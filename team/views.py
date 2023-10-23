from typing import List

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from team.models import Team
from team.serializers import TeamSerializer


# Only for documentation endpoints details
@extend_schema_view(
    create=extend_schema(
        description=(
            "Endpoint for creating Team by Admin user."
        )
    ),
    retrieve=extend_schema(
        description=(
            "Endpoint with detailed Team's page by id "
            "for Authenticated users."
        )
    ),
    update=extend_schema(
        description=(
            "Endpoint for updating a specific Team details "
            "by id for Admin users."
        )
    ),
    partial_update=extend_schema(
        description=(
            "Endpoint for partially updating a specific Team details "
            "by id for Admin users."
        )
    ),
    destroy=extend_schema(
        description=(
            "Endpoint for deleting a specific Team by id for Admin users."
        )
    ),
    list=extend_schema(
        description="Endpoint for listing all Teams for Authenticated users."
    ),
)
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes_by_action = {
        "default": (IsAdminUser,),
        "list": (IsAuthenticated,),
        "retrieve": (IsAuthenticated,),
    }

    @staticmethod
    def _instantiate_permissions(
            permissions: List
    ) -> List[IsAdminUser | IsAuthenticated]:
        """Instantiate and return the provided permission classes."""

        return [permission() for permission in permissions]

    def get_permissions(self) -> List[IsAdminUser | IsAuthenticated]:
        """
        Get permissions according to the action attribute.
        Fall back to default permissions if the action isn't recognised.
        """

        permissions = self.permission_classes_by_action.get(
            self.action,
            self.permission_classes_by_action["default"],
        )

        return self._instantiate_permissions(permissions)

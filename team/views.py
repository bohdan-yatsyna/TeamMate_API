from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from team.models import Team
from team.serializers import TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes_by_action = {
        "default": (IsAdminUser,),
        "list": (IsAuthenticated,),
        "retrieve": (IsAuthenticated,),
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission
                in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [
                permission()
                for permission in self.permission_classes_by_action["default"]
            ]

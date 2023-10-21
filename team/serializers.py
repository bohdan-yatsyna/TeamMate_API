from rest_framework import serializers

from person.models import Person
from team.models import Team


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Person.objects.all(),
        source="people",
    )

    class Meta:
        model = Team
        fields = ("id", "name", "members")

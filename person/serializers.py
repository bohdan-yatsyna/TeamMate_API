from django.contrib.auth import get_user_model
from rest_framework import serializers


class CreatePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "first_name", "last_name", "team")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
            }
        }

    def create(self, validated_data):
        """Create a new Person(user) with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class ManagePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
            "team"
        )
        read_only_fields = ("is_staff", "email", "id")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "required": False
            }
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance

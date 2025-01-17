from rest_framework import serializers
from django.core.exceptions import ValidationError

from roles.models import Role
from workspaces.models import Workspace, WorkspaceMember


class WorkspaceSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        user_id = self.context["request"].user.id
        name = attrs.get("name")

        if (
            WorkspaceMember.objects.select_related("workspace", "role")
            .filter(workspace__name=name, user_id=user_id, role__name="Owner")
            .exists()
        ):
            raise ValidationError(
                {
                    "name": f"A workspace with the name '{name}' already exists for this user."
                }
            )

        return attrs

    class Meta:
        model = Workspace
        fields = "__all__"


class WorkspaceMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkspaceMember
        fields = "__all__"

    def validate_role(self, value):
        if value.name == "Owner":
            raise ValidationError("This workspace already has an Owner.")

        return value
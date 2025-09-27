from rest_framework import serializers
from .models import Workspace, Project

class WorkspaceSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'owner', 'owner_username', 'owner_email', 'member_count', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.count()

    def create(self, validated_data):
        # Set the owner to the current user
        validated_data['owner'] = self.context['request'].user
        workspace = Workspace.objects.create(**validated_data)
        # Add the owner as a member
        workspace.members.add(self.context['request'].user)
        return workspace

class ProjectSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    workspace_name = serializers.CharField(source='workspace.name', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'workspace', 'workspace_name', 'created_by', 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['workspace', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
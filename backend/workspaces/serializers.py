# from rest_framework import serializers
# from .models import Workspace, Project, WorkspaceMember, Task
# from django.contrib.auth import get_user_model

# User = get_user_model()


# # ---- User Serializer (for members / owner display) ----
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']


# # ---- Workspace Member ----
# class WorkspaceMemberSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     user_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), source='user', write_only=True, required=False
#     )

#     class Meta:
#         model = WorkspaceMember
#         fields = ['id', 'user', 'user_id', 'role']


# # ---- Task ----
# class TaskSerializer(serializers.ModelSerializer):
#     assigned_to = UserSerializer(read_only=True)
#     assigned_to_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
#     )

#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'description', 'status', 'assigned_to', 'assigned_to_id', 'created_at']


# # ---- Workspace ----
# class WorkspaceSerializer(serializers.ModelSerializer):
#     owner_username = serializers.CharField(source='owner.username', read_only=True)
#     owner_email = serializers.CharField(source='owner.email', read_only=True)
#     member_count = serializers.SerializerMethodField()
#     members = WorkspaceMemberSerializer(source="workspacemember_set", many=True, read_only=True)
#     projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     tasks = serializers.SerializerMethodField() 

#     class Meta:
#         model = Workspace
#         fields = [
#             'id', 'name', 'description',
#             'owner', 'owner_username', 'owner_email',
#             'member_count', 'members', 'projects',
#             'tasks', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['owner', 'created_at', 'updated_at']

#     def get_member_count(self, obj):
#         return obj.members.count()

#     def create(self, validated_data):
#         # Set owner to current user
#         validated_data['owner'] = self.context['request'].user
#         workspace = Workspace.objects.create(**validated_data)
#         # Add owner as a member with role "owner"
#         WorkspaceMember.objects.create(
#             workspace=workspace,
#             user=self.context['request'].user,
#             role="owner"
#         )
#         return workspace
    
#     def get_tasks(self, obj):  
#         tasks = Task.objects.filter(project__workspace=obj)
#         return TaskSerializer(tasks, many=True).data


# # ---- Project ----
# class ProjectSerializer(serializers.ModelSerializer):
#     created_by_username = serializers.CharField(source='created_by.username', read_only=True)
#     workspace_name = serializers.CharField(source='workspace.name', read_only=True)
#     tasks = TaskSerializer(many=True, read_only=True)

#     class Meta:
#         model = Project
#         fields = [
#             'id', 'name', 'description',
#             'workspace', 'workspace_name',
#             'created_by', 'created_by_username',
#             'tasks',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['workspace', 'created_by', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         validated_data['created_by'] = self.context['request'].user
#         return super().create(validated_data)

from rest_framework import serializers
from .models import Workspace, Project, WorkspaceMember, Task
from django.contrib.auth import get_user_model

User = get_user_model()


# ---- User Serializer (for members / owner display) ----
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ---- Workspace Member ----
class WorkspaceMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True, required=False
    )

    class Meta:
        model = WorkspaceMember
        fields = ['id', 'user', 'user_id', 'role']


# ---- Task ----
class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to', 'assigned_to_id', 'created_at']
        read_only_fields = ['created_at']


# ---- Workspace ----
class WorkspaceSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    member_count = serializers.SerializerMethodField()
    members = WorkspaceMemberSerializer(source="workspacemember_set", many=True, read_only=True)
    projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)  # <-- direct relation now

    class Meta:
        model = Workspace
        fields = [
            'id', 'name', 'description',
            'owner', 'owner_username', 'owner_email',
            'member_count', 'members', 'projects',
            'tasks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.count()

    def create(self, validated_data):
        # Set owner to current user
        validated_data['owner'] = self.context['request'].user
        workspace = Workspace.objects.create(**validated_data)
        # Add owner as a member with role "owner"
        WorkspaceMember.objects.create(
            workspace=workspace,
            user=self.context['request'].user,
            role="owner"
        )
        return workspace


# ---- Project ----
class ProjectSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    workspace_name = serializers.CharField(source='workspace.name', read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description',
            'workspace', 'workspace_name',
            'created_by', 'created_by_username',
            'tasks',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['workspace', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


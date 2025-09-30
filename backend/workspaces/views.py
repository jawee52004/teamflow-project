from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Workspace, Project, WorkspaceMember, Task
from .serializers import (
    WorkspaceSerializer,
    ProjectSerializer,
    WorkspaceMemberSerializer,
    TaskSerializer
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_auth(request):
    return Response({
        'message': 'Authentication successful!',
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email
        }
    })


# ----------------- WORKSPACES -----------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workspace_list(request):
    

    if request.method == 'GET':
        workspaces = Workspace.objects.filter(members=request.user)
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkspaceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def workspace_detail(request, pk):
    workspace = get_object_or_404(Workspace, pk=pk, members=request.user)

    

    
    if request.method == 'GET':
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if workspace.owner != request.user:
            return Response({"error": "Only the owner can update the workspace"}, status=status.HTTP_403_FORBIDDEN)

        serializer = WorkspaceSerializer(workspace, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if workspace.owner != request.user:
            return Response({"error": "Only the owner can delete the workspace"}, status=status.HTTP_403_FORBIDDEN)

        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    



# ----------------- PROJECTS -----------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def project_list(request, workspace_id):
    workspace = get_object_or_404(Workspace, pk=workspace_id, members=request.user)

    

    if request.method == 'GET':
        projects = workspace.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(workspace=workspace)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('Project creation errors:', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def project_detail(request, workspace_id, pk):

    workspace = get_object_or_404(Workspace, pk=workspace_id, members=request.user)
    project = get_object_or_404(workspace.projects, pk=pk)

    

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if project.created_by != request.user:
            return Response({"error": "Only the creator can update the project"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectSerializer(project, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if project.created_by != request.user:
            return Response({"error": "Only the creator can delete the project"}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------- MEMBERS -----------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workspace_members(request, workspace_id):
    workspace = get_object_or_404(Workspace, pk=workspace_id, members=request.user)

    

    if request.method == 'GET':
        members = WorkspaceMember.objects.filter(workspace=workspace)
        serializer = WorkspaceMemberSerializer(members, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if workspace.owner != request.user:
            return Response({"error": "Only the owner can add members"}, status=status.HTTP_403_FORBIDDEN)

        serializer = WorkspaceMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(workspace=workspace)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- TASKS -----------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request, workspace_id):
    workspace = get_object_or_404(Workspace, pk=workspace_id, members=request.user)

    

    if request.method == 'GET':
        tasks = Task.objects.filter(project__workspace=workspace)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(workspace=workspace)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, workspace_id, pk):
    workspace = get_object_or_404(Workspace, pk=workspace_id, members=request.user)
    task = get_object_or_404(Task, pk=pk, project__workspace=workspace)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

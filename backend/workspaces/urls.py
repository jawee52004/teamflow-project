from django.urls import path
from . import views

urlpatterns = [
    path('test-auth/', views.test_auth, name='test-auth'),

    # Workspaces
    path('workspaces/', views.workspace_list, name='workspace-list'),
    path('workspaces/<int:pk>/', views.workspace_detail, name='workspace-detail'),

    # Projects
    path('workspaces/<int:workspace_id>/projects/', views.project_list, name='project-list'),
    path('workspaces/<int:workspace_id>/projects/<int:pk>/', views.project_detail, name='project-detail'),

    # Members
    path('workspaces/<int:workspace_id>/members/', views.workspace_members, name='workspace-members'),

    # Tasks
    path('workspaces/<int:workspace_id>/tasks/', views.task_list, name='task-list'),
    path('workspaces/<int:workspace_id>/tasks/<int:pk>/', views.task_detail, name='task-detail'),
]

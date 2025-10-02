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

    # Invitations
    path('workspaces/<int:workspace_id>/invite/', views.invite_member, name='invite-member'),
    path('workspaces/invitations/accept/<uuid:token>/', views.accept_invitation, name='accept-invitation'),

    # Members
    path('workspaces/<int:workspace_id>/members/', views.workspace_members, name='workspace-members'),
    path('workspaces/<int:workspace_id>/members/<int:member_id>/', views.workspace_member_detail, name='workspace-member-detail'), 
    path('workspaces/<int:workspace_id>/invite/', views.invite_member, name='invite_member'),
    path('invitations/<uuid:token>/accept/', views.accept_invitation, name='accept-invite'), 
    
    # Tasks
    path('workspaces/<int:workspace_id>/tasks/', views.task_list, name='task-list'),
    path('workspaces/<int:workspace_id>/tasks/<int:pk>/', views.task_detail, name='task-detail'),
]

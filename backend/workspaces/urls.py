from django.urls import path
from . import views

urlpatterns = [
    path('test-auth/', views.test_auth, name='test-auth'),
    path('workspaces/', views.workspace_list, name='workspace-list'),
    path('workspaces/<int:pk>/', views.workspace_detail, name='workspace-detail'),
    path('workspaces/<int:workspace_id>/projects/', views.project_list, name='project-list'),
    path('workspaces/<int:workspace_id>/projects/<int:pk>/', views.project_detail, name='project-detail'),
]
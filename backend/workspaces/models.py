# from django.db import models
# from django.conf import settings

# User = settings.AUTH_USER_MODEL

# class Workspace(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
#     members = models.ManyToManyField(User, through='WorkspaceMember', related_name='workspaces')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class WorkspaceMember(models.Model):
#     ROLE_CHOICES = [
#         ('owner', 'Owner'),
#         ('developer', 'Developer'),
#         ('viewer', 'Viewer'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='developer')

#     class Meta:
#         unique_together = ('user', 'workspace')


# class Project(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='projects')
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class Task(models.Model):
#     STATUS_CHOICES = [
#         ('TODO', 'To Do'),
#         ('IN_PROGRESS', 'In Progress'),
#         ('DONE', 'Done'),
#     ]

#     title = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
#     assigned_to = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
#     )
#     project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Workspace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
    members = models.ManyToManyField(User, through='WorkspaceMember', related_name='workspaces')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkspaceMember(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('developer', 'Developer'),
        ('viewer', 'Viewer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='developer')

    class Meta:
        unique_together = ('user', 'workspace')


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='projects')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    # 👇 NEW: connect tasks directly to a workspace
    workspace = models.ForeignKey(Workspace, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)
    # project remains optional
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
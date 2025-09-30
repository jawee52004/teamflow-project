from django.apps import AppConfig

class WorkspacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workspaces'

    
    def landing_page(request):
        return render(request, "landing.html")

    def login_page(request):
        return render(request, "login.html")

    def register_page(request):
        return render(request, "register.html")

    def workspace_page(request):
        return render(request, "workspace.html")
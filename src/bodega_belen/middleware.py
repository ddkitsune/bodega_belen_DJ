from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AutoLoginMiddleware:
    """
    Middleware para auto-login (Modo quiosco/negocio pequeño).
    Si el usuario no está autenticado, lo loguea automáticamente como 'admin'.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Buscar o crear usuario por defecto
            try:
                user = User.objects.filter(username='admin').first()
                if not user:
                    # Crear admin si no existe
                    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
                
                # Forzar login sin contraseña
                # Especificar el backend es necesario para login() manual
                if not hasattr(user, 'backend'):
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                
                login(request, user)
            except Exception as e:
                # Si falla (ej. DB no lista), fallar silenciosamente y dejar que Django maneje
                pass

        # Si intenta ir al login y ya está logueado, mandar al dashboard
        if request.path == reverse('login') and request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return self.get_response(request)

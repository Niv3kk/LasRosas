# backend/api/auth_backend.py
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.apps import apps

from .jwt_utils import decode_jwt  # 👈 importante: NO importamos auth_views aquí


class UsuarioJWTAuthentication(BaseAuthentication):
    """
    Autenticación personalizada que:
    - Lee 'Authorization: Bearer <token>'
    - Decodifica el token con decode_jwt
    - Busca al Usuario (modelo de 'api') usando el 'sub' del payload
    - Coloca ese Usuario en request.user
    """

    def authenticate(self, request):
        # Puedes usar request.headers o get_authorization_header, las dos valen.
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            # No hay token -> DRF prueba otras auth classes (si las hay) o deja user como Anonymous
            return None

        token = auth_header.split(' ', 1)[1].strip()
        if not token:
            raise exceptions.AuthenticationFailed('Token vacío')

        # Decodificar el JWT
        try:
            payload = decode_jwt(token)
        except Exception:
            raise exceptions.AuthenticationFailed('Token inválido o expirado')

        user_id = payload.get('sub')
        if not user_id:
            raise exceptions.AuthenticationFailed('Token sin identificador de usuario')

        Usuario = apps.get_model('api', 'Usuario')
        try:
            usuario = Usuario.objects.select_related('rol').get(usuario_id=int(user_id))
        except Usuario.DoesNotExist:
            raise exceptions.AuthenticationFailed('Usuario no encontrado')

        # 🔴 Parche importante: DRF espera que el user tenga .is_authenticated
        # Lo añadimos dinámicamente sin tocar el modelo ni la base de datos.
        setattr(usuario, 'is_authenticated', True)

        # DRF espera un tuple (user, auth)
        return (usuario, None)

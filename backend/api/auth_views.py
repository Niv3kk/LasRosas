# backend/api/auth_views.py
import hashlib
import jwt
from django.conf import settings
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UsuarioSerializer
from .security import check_pwd 
from .jwt_utils import create_jwt, decode_jwt  


def get_usuario_model():
    """Importación perezosa para evitar problemas de orden de carga."""
    return apps.get_model('api', 'Usuario')


class LoginView(APIView):
    # Endpoint público: no requiere autenticación previa
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        Usuario = get_usuario_model()
        username = (request.data.get('username') or '').strip()
        password = request.data.get('password') or ''
        if not username or not password:
            return Response({'detail': 'Usuario y contraseña son obligatorios.'}, status=400)

        try:
            user = Usuario.objects.select_related('rol').get(nombre_usuario=username)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuario o contraseña incorrectos.'}, status=401)

        if not check_pwd(password, user.hash_contrasena):
            return Response({'detail': 'Usuario o contraseña incorrectos.'}, status=401)

        user_data = UsuarioSerializer(user).data
        access = create_jwt({
            'sub': user.usuario_id,          
            'username': user.nombre_usuario,
            'role': user.rol.nombre_rol,
        }, minutes=60)

        return Response({'access': access, 'user': user_data}, status=200)


class MeView(APIView):
    # Usamos la autenticación por defecto (UsuarioJWTAuthentication) definida en settings.py
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Gracias al authentication backend, request.user ya es una instancia de Usuario
        user = request.user
        data = UsuarioSerializer(user).data
        return Response(data, status=200)


# =========================
# Endpoints de diagnóstico (TEMPORAL — puedes borrarlos luego)
# =========================

def _key_fingerprint():
    """Huella de la SECRET_KEY para confirmar que es estable sin exponerla."""
    return hashlib.sha256((settings.SECRET_KEY or "").encode()).hexdigest()[:12]


class DiagKeyView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"key_fingerprint": _key_fingerprint()}, status=200)


class DiagTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        auth = request.headers.get('Authorization', '')
        token = auth.split(' ', 1)[1] if auth.startswith('Bearer ') else ''
        if not token:
            return Response({"error": "no token"}, status=400)

        # payload sin verificar (para inspeccionar)
        try:
            noverify = jwt.decode(
                token,
                options={"verify_signature": False, "verify_exp": False, "verify_iat": False},
                algorithms=["HS256"]
            )
        except Exception as e:
            return Response({"stage": "decode_noverify", "error": type(e).__name__, "msg": str(e)}, status=400)

        # validación real con SECRET_KEY del proceso (reusamos decode_jwt del módulo)
        try:
            verified = decode_jwt(token)
            return Response({
                "key_fingerprint": _key_fingerprint(),
                "verified": True,
                "payload": verified,
                "noverify": noverify,
            }, status=200)
        except Exception as e:
            return Response({
                "key_fingerprint": _key_fingerprint(),
                "verified": False,
                "error_type": type(e).__name__,
                "error_msg": str(e),
                "noverify": noverify,
            }, status=401)

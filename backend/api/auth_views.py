# backend/api/auth_views.py
import datetime
import hashlib
import jwt
from django.conf import settings
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UsuarioSerializer
from .security import check_pwd  # si no lo tienes, avísame y te paso uno básico


def get_usuario_model():
    """Importación perezosa para evitar problemas de orden de carga."""
    return apps.get_model('api', 'Usuario')


def create_jwt(payload: dict, minutes=60):
    """Crea un JWT con exp/iat. Fuerza sub a string (PyJWT v2 requiere str)."""
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    to_encode = {**payload, 'exp': exp, 'iat': datetime.datetime.utcnow()}
    if 'sub' in to_encode:
        to_encode['sub'] = str(to_encode['sub'])
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')


def decode_jwt(token: str):
    """Valida el JWT con leve tolerancia de reloj."""
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=['HS256'],
        options={"require": ["exp", "iat"]},
        leeway=10,  # ±10s por si el reloj está levemente desfasado
    )


class LoginView(APIView):
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
            'sub': user.usuario_id,          # puede venir int; adentro se fuerza a str
            'username': user.nombre_usuario,
            'role': user.rol.nombre_rol,
        }, minutes=60)

        return Response({'access': access, 'user': user_data}, status=200)


class MeView(APIView):
    def get(self, request):
        Usuario = get_usuario_model()
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return Response({'detail': 'No autorizado'}, status=401)

        token = auth.split(' ', 1)[1]
        try:
            payload = decode_jwt(token)
        except Exception:
            return Response({'detail': 'Token inválido/expirado'}, status=401)

        # sub viene como string en el token; casteamos a int para la consulta
        user_id = payload.get('sub')
        try:
            user = Usuario.objects.select_related('rol').get(usuario_id=int(user_id))
        except (Usuario.DoesNotExist, ValueError, TypeError):
            return Response({'detail': 'Usuario no encontrado'}, status=404)

        return Response(UsuarioSerializer(user).data, status=200)


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

        # validación real con SECRET_KEY del proceso
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

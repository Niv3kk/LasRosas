# backend/api/serializers.py
from rest_framework import serializers
from .models import (
    Historialinventario,
    Inventario,
    Usuario,   # modelo usado para autenticación
    Usuarios,  # modelo que usa el FK de Historialinventario
)
from django.utils import timezone

"""
Login 
"""

class RolSerializer(serializers.Serializer):
    rol_id = serializers.IntegerField()
    nombre_rol = serializers.CharField()
    descripcion_permisos = serializers.CharField(allow_null=True, allow_blank=True)


class UsuarioSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    nombre_completo = serializers.CharField()
    nombre_usuario = serializers.CharField()
    rol = RolSerializer()


"""
Inventario y Historial de inventario 
"""

class InventarioSerializer(serializers.ModelSerializer):
    stock_actual = serializers.IntegerField(read_only=True)

    # Mapeamos 'id' a la PK real del modelo (aunque se llame inventario_id)
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = Inventario
        fields = ['id', 'nombre_articulo', 'detalle', 'stock_actual']



class HistorialInventarioSerializer(serializers.ModelSerializer):
    # --- Campos de LECTURA ---
    nombre_articulo = serializers.CharField(
        source='inventario.nombre_articulo',
        read_only=True
    )

    # Lo calculamos a mano para ser flexibles
    nombre_usuario = serializers.SerializerMethodField()
    fecha = serializers.DateTimeField(read_only=True)

    # ID amigable para el front
    id = serializers.IntegerField(source='pk', read_only=True)

    # --- Campo de ESCRITURA ---
    inventario = serializers.PrimaryKeyRelatedField(
        queryset=Inventario.objects.all()
    )

    class Meta:
        model = Historialinventario
        fields = [
            'id',
            'fecha',
            'tipo_movimiento',
            'cantidad',
            'motivo',
            'inventario',
            'nombre_articulo',
            'nombre_usuario',
        ]
        extra_kwargs = {
            'motivo': {'required': True, 'allow_blank': False},
            'tipo_movimiento': {'required': True, 'allow_blank': False},
        }

    def create(self, validated_data):
        """
        Asigna fecha actual y mapea request.user (Usuario)
        al modelo que el FK espera (Usuarios).
        """
        request = self.context.get('request')

        # Si tenemos request y el usuario es del modelo Usuario (login)
        if request and hasattr(request, 'user') and isinstance(request.user, Usuario):
            u_login = request.user

            try:
                # Mapeo Usuario -> Usuarios usando usuario_id (comparten ID)
                usuario_hist = Usuarios.objects.get(usuario_id=u_login.usuario_id)
                validated_data['usuario'] = usuario_hist
            except Usuarios.DoesNotExist:
                # Si no hay coincidencia, dejamos usuario vacío (se verá como "Sistema")
                pass

        # Fecha actual
        validated_data['fecha'] = timezone.now()
        return super().create(validated_data)

    def get_nombre_usuario(self, obj):
        """
        Devuelve el nombre del usuario que hizo el movimiento.
        Si no hay usuario, devolvemos 'Sistema'.
        """
        u = getattr(obj, 'usuario', None)
        if not u:
            return 'Sistema'

        # Usuarios tiene nombre_completo y nombre_usuario
        return (
            getattr(u, 'nombre_completo', None)
            or getattr(u, 'nombre_usuario', None)
            or str(u)
        )
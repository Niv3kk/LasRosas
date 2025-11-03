# backend/api/serializers.py
from rest_framework import serializers

# NOTA: Usamos Serializer simple (no ModelSerializer) para evitar importar api.models

class RolSerializer(serializers.Serializer):
    rol_id = serializers.IntegerField()
    nombre_rol = serializers.CharField()
    descripcion_permisos = serializers.CharField(allow_null=True, allow_blank=True)

class UsuarioSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    nombre_completo = serializers.CharField()
    nombre_usuario = serializers.CharField()
    rol = RolSerializer()
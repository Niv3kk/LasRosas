# backend/api/models.py
from django.db import models

class Rol(models.Model):
    rol_id = models.AutoField(primary_key=True)
    nombre_rol = models.TextField()
    descripcion_permisos = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'
        app_label = 'api'  # ayuda extra si hiciera falta

class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='rol_id', related_name='usuarios')
    nombre_completo = models.TextField()
    nombre_usuario = models.TextField(unique=True)
    hash_contrasena = models.TextField()

    class Meta:
        managed = False
        db_table = 'usuarios'
        app_label = 'api'

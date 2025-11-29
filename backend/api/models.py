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


class Alquileres(models.Model):
    alquiler_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Clientes', models.DO_NOTHING)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    fecha_evento = models.DateField(blank=True, null=True)
    estado = models.TextField()
    garantia_tipo = models.TextField(blank=True, null=True)
    garantia_valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    garantia_descripcion = models.TextField(blank=True, null=True)
    garantia_devuelta = models.BooleanField(blank=True, null=True)
    total_orden_alquiler = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_orden_danos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_recojo = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alquileres'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Clientes(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nombre_completo = models.TextField()
    telefono = models.TextField()

    class Meta:
        managed = False
        db_table = 'clientes'


class DetalleAlquiler(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    alquiler = models.ForeignKey(Alquileres, models.DO_NOTHING)
    inventario = models.ForeignKey('Inventario', models.DO_NOTHING)
    cantidad_alquilada = models.IntegerField()
    direccion_entrega = models.TextField(blank=True, null=True)
    precio_alquiler_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    precio_danos_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_alquiler = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_devuelta_ok = models.IntegerField(blank=True, null=True)
    cantidad_danada = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_alquiler'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Historialinventario(models.Model):
    historial_id = models.AutoField(primary_key=True)
    inventario = models.ForeignKey('Inventario', models.DO_NOTHING)
    fecha = models.DateTimeField(blank=True, null=True)
    tipo_movimiento = models.TextField()
    cantidad = models.IntegerField()
    motivo = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    detalle = models.ForeignKey(DetalleAlquiler, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historialinventario'


class Inventario(models.Model):
    inventario_id = models.AutoField(primary_key=True)
    nombre_articulo = models.TextField(unique=True)
    detalle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'


# models.py

class Listapreciosalquiler(models.Model):
    precio_alquiler_id = models.AutoField(primary_key=True)
    inventario = models.ForeignKey('Inventario', models.DO_NOTHING,
                                   db_column='inventario_id', related_name='precios_alquiler')
    nombre_tarifa = models.TextField()
    unidades_incluidas = models.IntegerField()
    precio_tarifa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False  # la tabla ya existe en Supabase
        db_table = 'listapreciosalquiler'


class Listapreciosdanos(models.Model):
    precio_dano_id = models.AutoField(primary_key=True)
    inventario = models.ForeignKey('Inventario', models.DO_NOTHING,
                                   db_column='inventario_id', related_name='precios_danos')
    nombre_tarifa = models.TextField()
    unidades_incluidas = models.IntegerField()
    precio_tarifa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'listapreciosdanos'
        
class Roles(models.Model):
    rol_id = models.AutoField(primary_key=True)
    nombre_rol = models.TextField(unique=True)
    descripcion_permisos = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Usuarios(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Roles, models.DO_NOTHING)
    nombre_completo = models.TextField()
    nombre_usuario = models.TextField(unique=True)
    hash_contrasena = models.TextField()

    class Meta:
        managed = False
        db_table = 'usuarios'

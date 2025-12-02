from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status # <--- Importación clave
from .models import Inventario, Historialinventario
from .serializers import InventarioSerializer, HistorialInventarioSerializer
from django.db.models import Sum, Case, When, F, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated # <--- NUEVA IMPORTACIÓN
from .models import Listapreciosalquiler, Listapreciosdanos
from .serializers import (
    ListaPreciosAlquilerSerializer,
    ListaPreciosDanosSerializer,
)

def health(request):
    """
    Endpoint simple para verificar que la app y la BD están conectadas.
    """
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1;")
            row = cur.fetchone()
        return JsonResponse({"ok": True, "db": "connected", "select_1": row[0]})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


# backend/api/views.py

class InventarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint que muestra y permite crear inventario
    con su stock actual calculado.
    """
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']  # evita delete/put si quieres

    def get_queryset(self):
        stock_calculado = Sum(
            Case(
                When(historialinventario__tipo_movimiento='Entrada', then=F('historialinventario__cantidad')),
                When(historialinventario__tipo_movimiento='Salida', then=F('historialinventario__cantidad') * -1),
                default=0,
                output_field=IntegerField()
            )
        )
        queryset = Inventario.objects.annotate(
            stock_actual=Coalesce(stock_calculado, 0)
        ).order_by('nombre_articulo')

        return queryset

    def create(self, request, *args, **kwargs):
        # Solo necesitamos nombre_articulo y detalle
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear el item en inventario
        inventario = serializer.save()

        # Crear tarifas por defecto en ALQUILER
        Listapreciosalquiler.objects.create(
            inventario=inventario,
            nombre_tarifa="Precio por Unidad",
            unidades_incluidas=1,
            precio_tarifa=0,
        )

        # Crear tarifas por defecto en DAÑOS / PÉRDIDAS
        Listapreciosdanos.objects.create(
            inventario=inventario,
            nombre_tarifa="Daño o pérdida",
            unidades_incluidas=1,
            precio_tarifa=0,
        )

        # Volvemos a cargar el item con el stock_actual calculado
        from django.db.models import Sum, Case, When, F, IntegerField
        from django.db.models.functions import Coalesce

        stock_calculado = Sum(
            Case(
                When(historialinventario__tipo_movimiento='Entrada', then=F('historialinventario__cantidad')),
                When(historialinventario__tipo_movimiento='Salida', then=F('historialinventario__cantidad') * -1),
                default=0,
                output_field=IntegerField()
            )
        )
        inventario_refresco = (
            Inventario.objects
            .annotate(stock_actual=Coalesce(stock_calculado, 0))
            .get(pk=inventario.pk)
        )

        output = self.get_serializer(inventario_refresco)
        return Response(output.data, status=status.HTTP_201_CREATED)


# --- CAMBIO IMPORTANTE AQUÍ ---
# 1. Cambiamos ReadOnlyModelViewSet por ModelViewSet
class HistorialinventarioViewSet(viewsets.ModelViewSet):
# ---------------------------------
    """
    API endpoint que muestra todo el historial de inventario.
    Ahora permite GET (listar) y POST (crear).
    """
    # 2. Ordenamos por fecha descendente (más nuevos primero)
    queryset = Historialinventario.objects.all().select_related('inventario', 'usuario').order_by('-fecha')
    serializer_class = HistorialInventarioSerializer
    filterset_fields = ['inventario', 'tipo_movimiento', 'usuario']
    # 3. Aseguramos que solo usuarios logueados puedan acceder
    permission_classes = [IsAuthenticated]
# -------------------------------------------------------------------
# Lista de precios de alquiler
# -------------------------------------------------------------------
class ListaPreciosAlquilerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            Listapreciosalquiler.objects
            .select_related('inventario')
            .order_by('inventario__nombre_articulo')
        )
        serializer = ListaPreciosAlquilerSerializer(qs, many=True)
        return Response(serializer.data)

    def put(self, request):
        """
        Actualiza la lista completa de precios de alquiler.
        """
        data = request.data

        # ids que vienen desde el frontend
        ids_enviados = [
            item.get("precio_alquiler_id")
            for item in data
            if item.get("precio_alquiler_id") is not None
        ]

        if ids_enviados:
            Listapreciosalquiler.objects.exclude(
                precio_alquiler_id__in=ids_enviados
            ).delete()
        else:
            Listapreciosalquiler.objects.all().delete()

        for item in data:
            pk = item.get("precio_alquiler_id")

            defaults = {
                "inventario_id": item["inventario_id"],
                "nombre_tarifa": item.get("nombre_tarifa") or "Precio por Unidad",
                "unidades_incluidas": item["unidades_incluidas"],
                "precio_tarifa": item["precio_tarifa"],
            }

            if pk:
                Listapreciosalquiler.objects.update_or_create(
                    precio_alquiler_id=pk,
                    defaults=defaults,
                )
            else:
                Listapreciosalquiler.objects.create(**defaults)

        qs = (
            Listapreciosalquiler.objects
            .select_related('inventario')
            .order_by('inventario__nombre_articulo')
        )
        serializer = ListaPreciosAlquilerSerializer(qs, many=True)
        return Response(serializer.data)


# -------------------------------------------------------------------
# Lista de precios de daños / pérdidas
# -------------------------------------------------------------------
class ListaPreciosDanosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            Listapreciosdanos.objects
            .select_related('inventario')
            .order_by('inventario__nombre_articulo')
        )
        serializer = ListaPreciosDanosSerializer(qs, many=True)
        return Response(serializer.data)

    def put(self, request):
        """
        Actualiza la lista completa de precios de daños.
        """
        data = request.data

        ids_enviados = [
            item.get("precio_dano_id")
            for item in data
            if item.get("precio_dano_id") is not None
        ]

        if ids_enviados:
            Listapreciosdanos.objects.exclude(
                precio_dano_id__in=ids_enviados
            ).delete()
        else:
            Listapreciosdanos.objects.all().delete()

        for item in data:
            pk = item.get("precio_dano_id")

            defaults = {
                "inventario_id": item["inventario_id"],
                "nombre_tarifa": item.get("nombre_tarifa") or item.get("detalle", ""),
                "unidades_incluidas": item["unidades_incluidas"],
                "precio_tarifa": item["precio_tarifa"],
            }

            if pk:
                Listapreciosdanos.objects.update_or_create(
                    precio_dano_id=pk,
                    defaults=defaults,
                )
            else:
                Listapreciosdanos.objects.create(**defaults)

        qs = (
            Listapreciosdanos.objects
            .select_related('inventario')
            .order_by('inventario__nombre_articulo')
        )
        serializer = ListaPreciosDanosSerializer(qs, many=True)
        return Response(serializer.data)

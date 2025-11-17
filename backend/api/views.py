from django.http import JsonResponse
from django.db import connection
from rest_framework import viewsets # <--- Importación clave
from .models import Inventario, Historialinventario
from .serializers import InventarioSerializer, HistorialInventarioSerializer
from django.db.models import Sum, Case, When, F, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated # <--- NUEVA IMPORTACIÓN

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


class InventarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que muestra todo el inventario CON su stock actual calculado.
    (Este se queda como ReadOnly)
    """
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated] # <--- Añadir permisos
    queryset = Inventario.objects.all() # Necesario para el serializer de abajo

    def get_queryset(self):
        # ... (Tu lógica de cálculo de stock se queda igual) ...
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
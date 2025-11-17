from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health
from . import views

# Importa tus vistas de auth personalizadas
from .auth_views import MeView, LoginView  

router = DefaultRouter()
router.register(r'inventario', views.InventarioViewSet, basename='inventario')
router.register(r'historial-inventario', views.HistorialinventarioViewSet, basename='historialinventario')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health, name='health'),

    # 🔴 Aquí usamos TU LoginView, no SimpleJWT
    path('auth/token/', LoginView.as_view(), name='auth-token'),

    # Tu endpoint para obtener datos del usuario logueado
    path('auth/me/', MeView.as_view(), name='auth-me'),

    # (Opcional) Endpoints de diagnóstico si los quieres exponer un rato:
    # path('auth/diag-key/', DiagKeyView.as_view(), name='diag-key'),
    # path('auth/diag-token/', DiagTokenView.as_view(), name='diag-token'),
]

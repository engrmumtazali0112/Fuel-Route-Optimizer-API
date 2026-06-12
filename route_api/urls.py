from django.urls import path
from .views import RouteOptimizeView, FuelPricesView, HealthCheckView

urlpatterns = [
    path('route/optimize/', RouteOptimizeView.as_view(), name='route-optimize'),
    path('route/fuel-prices/', FuelPricesView.as_view(), name='fuel-prices'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]

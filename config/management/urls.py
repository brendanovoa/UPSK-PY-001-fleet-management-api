from django.urls import path
from .views import list_taxis, obtener_ubicaciones_taxi

urlpatterns = [
    path('api/taxis/', list_taxis, name='list_taxis'),
    path('api/obtener-ubicaciones-taxi/', obtener_ubicaciones_taxi, name='obtener_ubicaciones_taxi'),
]

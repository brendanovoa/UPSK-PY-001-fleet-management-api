from django.urls import path
from .views import list_taxis

urlpatterns = [
    path('api/taxis/', list_taxis, name='list_taxis'),
]

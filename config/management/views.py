from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import JsonResponse
from .models import taxis, trajectories
# from .serializers import TaxisSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg import openapi

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Obtiene la lista de taxis.",
    responses={200: 'OK', 400: 'Bad Request', 404: 'Not Found'},
    manual_parameters=[
        openapi.Parameter(
            name='page',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='Número de página a recuperar.'
        ),
    ]
)

def list_taxis(request):
    try:
        all_taxis = taxis.objects.all() 
        # Realiza consulta a base de datos para obtener los objetos de modelo taxis

        # Paginación
        page_size = 10
        paginator = Paginator(all_taxis, page_size)
        page_number = request.GET.get('page')

        try:
            taxis_page = paginator.page(page_number)
        except PageNotAnInteger:
            # Si el parametro de pagina no es un entero, mostrar la pagina 1 
            taxis_page = paginator.page(1)
        except EmptyPage:
            # Si el numero de pagina esta fuera de rango mostrar la ultima pagina
            taxis_page = paginator.page(paginator.num_pages)

        taxis_data = [{
            'id': taxi.id,
            'placa': taxi.plate
        } for taxi in taxis_page]

        # Construir la respuesta paginada
        response_data = {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'page_number': taxis_page.number,
            'has_next': taxis_page.has_next(),
            'has_previous': taxis_page.has_previous(),
            'results': taxis_data
        }

        return Response(response_data, status=200) 
    except Exception as e:
        error_message = "Error al obtener la lista de taxis: " + str(e)
        return Response({"error": error_message}, status=400) 

    # return JsonResponse(taxis_data, safe=False)
    # return Response(taxis_data, status=200)

    # taxis_serializer = TaxisSerializer(taxis_page, many=True)
    # taxis_data = taxis_serializer.data

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Obtiene las ubicaciones de un taxi dado su ID y una fecha.",
    responses={200: 'OK', 400: 'Bad Request', 404: 'Not Found'},
    manual_parameters=[
        openapi.Parameter(
            name='id_taxi',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='ID del taxi.'
        ),
        openapi.Parameter(
            name='fecha',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Fecha en formato YYYY-MM-DD.'
        ),
    ]
)

def obtener_ubicaciones_taxi(request):
    try:
        id_taxi = request.GET.get('id_taxi')
        #self.request.query_params.get('taxi_id')
        fecha = request.GET.get('fecha')

        # Consulta a la base de datos para obtener las ubicaciones del taxi dado su ID y fecha
        ubicaciones = trajectories.objects.filter(taxi_id=id_taxi, date=fecha)

        ubicaciones_data = [{
            'latitud': ubicacion.latitud,
            'longitud': ubicacion.longitud,
            'timestamp': ubicacion.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for ubicacion in ubicaciones]

        return Response(ubicaciones_data, status=200) 
    except Exception as e:
        error_message = "Error al obtener las ubicaciones del taxi: " + str(e)
        return Response({"error": error_message}, status=400) 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from bmstu_lab.models import Services, Applications, ServicesApplications
from api.serializers import ApplicationsSerializer
from api.serializers import ServicesSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator, ReadOnly


def filter_applications_for_role(user):
    qs=Applications.objects.all()
    qs=qs.filter(Q(user=user) | Q(moderator=user))
    if user.user_role=='US':
        qs=qs.exclude(status=Applications.DELETED)
    return qs

def filter_services_for_role(user):
    qs=Services.objects.all()
    if not user.is_anonymous and user.user_role=='US':
        qs=qs.exclude(published=False)
    return qs


@api_view()
def order_list(request):
    object_list = Services.objects.filter(published=True)
    return Response(
    [{
        'id': obj.id,
        'name': obj.name,
        'image': obj.image.url,
        'text': obj.text,
        'type': obj.get_type_display(),
        'price': obj.price,
    } for obj in object_list]
    )


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def application_list(request):
    if request.method == 'GET':
        object_list = filter_applications_for_role(request.user)
        serializer = ApplicationsSerializer(object_list, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ApplicationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = ApplicationsSerializer(object_list)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def application_detail(request, id):
    object_list = filter_applications_for_role(request.user)
    obj=get_object_or_404(object_list, pk=id)
    if request.method == 'GET':
        serializer = ApplicationsSerializer(obj)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ApplicationsSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        obj.status=obj.DELETED
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated | ReadOnly])
def services_list(request):
    if request.method == 'GET':
        object_list = filter_services_for_role(request.user)
        serializer = ServicesSerializer(object_list, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ServicesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        serializer = ServicesSerializer(object_list)
    
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated | ReadOnly])
def services_detail(request, id):
    object_list = filter_services_for_role(request.user)
    obj=get_object_or_404(object_list, pk=id)
    if request.method == 'GET':
        serializer = ServicesSerializer(obj)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ServicesSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.status=obj.DELETED
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def service_to_application(request, id, application_id):
    services_list = filter_services_for_role(request.user)
    service=get_object_or_404(services_list, pk=id)
    application_list = filter_applications_for_role(request.user)
    application=get_object_or_404(application_list, pk=application_id)
    application.services.add(service)
    return Response(status=status.HTTP_204_NO_CONTENT)
    



@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsModerator])
@csrf_exempt
def delete_service(request, id, service_id):
    # services_list = Services.objects.exclude(published=False)
    # service=get_object_or_404(services_list, pk=service_id)
    # application_list = Applications.objects.filter(Q(user=request.user) | Q(moderator=request.user)).exclude(status=Applications.DELETED)
    application=get_object_or_404(ServicesApplications.objects.all(), applications_id=id, services_id=service_id )
    application.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    

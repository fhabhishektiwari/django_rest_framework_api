from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.

@api_view(['GET'])
def home(request):
    student_objs=Student.objects.all()
    serializer= StudentSerializers(student_objs,many=True)
    return Response({
        'status':200,
        'payload':serializer.data,
    })


@api_view(['POST'])
def post_student(request):
    data=request.data
    serializer = StudentSerializers(data=data)
    if not serializer.is_valid():
        return Response({
            'status': 403,
            'errors':serializer.errors,
            'message': 'Something went wrong...'
        })
    serializer.save()
    return Response({
        'status': 200,
        'payload': serializer.data,
        'message':'you sent'
    })


@api_view(['PUT'])
def update_student(request,id):
    try:
        student_obj=Student.objects.get(id=id)
        serializer = StudentSerializers(student_obj,data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'Something went wrong...'
            })
        serializer.save()
        return Response({
            'status': 200,
            'payload': serializer.data,
            'message': 'you sent'
        })
    except Exception as e:
        return Response({
            'status':403,
            'message':'invalid Id'
        })

@api_view(['DELETE'])
def delete_student(request,id):
    try:
        student_obj=Student.objects.get(id=id)
        student_obj.delete()
        return Response({
            'status': 200,
            'message': 'Deleted...'
        })
    except Exception as e:
        return Response({
            'status': 403,
            'message': 'invalid Id'
        })

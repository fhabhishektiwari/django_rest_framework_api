from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


@api_view(['GET'])
def get_book(request):
    book_obj = Book.objects.all()
    serializer = BookSerializers(book_obj, many=True)
    return Response({
        'status': 200,
        'payload': serializer.data
    })

# Register user
class RegisterUser(APIView):
    def post(self,request):
        serializer=UserSerializers(data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'Something went wrong...'
            })
        serializer.save()
        
        user=User.objects.get(username=serializer.data['username'])
        # token_obj,_= Token.objects.get_or_create(user=user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 200,
            'payload': serializer.data,
            # 'token':str(token_obj),
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'you sent'
        })




class StudentAPI(APIView):

    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_objs = Student.objects.all()
        serializer = StudentSerializers(student_objs, many=True)
        # get user who can access api
        print(request.user)

        return Response({
            'status': 200,
            'payload': serializer.data,
        })

    def post(self, request):
        data = request.data
        serializer = StudentSerializers(data=data)
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

    def put(self, request):
        pass

    def patch(self, request):
        try:
            student_obj = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializers(student_obj, data=request.data,partial=True)
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
                'message': 'Data Updated'
            })
        except Exception as e:
            return Response({
                'status':403,
                'message':'invalid Id'
            })

    def delete(self, request):
        try:
            id=request.GET.get('id')
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


# @api_view(['GET'])
# def home(request):
#     student_objs=Student.objects.all()
#     serializer= StudentSerializers(student_objs,many=True)
#     return Response({
#         'status':200,
#         'payload':serializer.data,
#     })


# @api_view(['POST'])
# def post_student(request):
#     data=request.data
#     serializer = StudentSerializers(data=data)
#     if not serializer.is_valid():
#         return Response({
#             'status': 403,
#             'errors':serializer.errors,
#             'message': 'Something went wrong...'
#         })
#     serializer.save()
#     return Response({
#         'status': 200,
#         'payload': serializer.data,
#         'message':'you sent'
#     })


# @api_view(['PUT'])
# def update_student(request,id):
#     try:
#         student_obj=Student.objects.get(id=id)
#         serializer = StudentSerializers(student_obj,data=request.data)
#         print(serializer)
#         if not serializer.is_valid():
#             return Response({
#                 'status': 403,
#                 'errors': serializer.errors,
#                 'message': 'Something went wrong...'
#             })
#         serializer.save()
#         return Response({
#             'status': 200,
#             'payload': serializer.data,
#             'message': 'you sent'
#         })
#     except Exception as e:
#         return Response({
#             'status':403,
#             'message':'invalid Id'
#         })

# @api_view(['DELETE'])
# def delete_student(request,id):
#     try:
#         student_obj=Student.objects.get(id=id)
#         student_obj.delete()
#         return Response({
#             'status': 200,
#             'message': 'Deleted...'
#         })
#     except Exception as e:
#         return Response({
#             'status': 403,
#             'message': 'invalid Id'
#         })

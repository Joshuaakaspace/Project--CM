from .serializer import *
from .models import *
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.permissions import IsAuthenticated
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

class LoginApi(APIView):

    @staticmethod
    def post(request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        try:
            if User.objects.filter(username=username).first():
                user = User.objects.filter(username=username).first()
                if password != "":
                    if check_password(password, user.password):
                        token, created = Token.objects.get_or_create(user=user)
                        params = {
                            'user_id': user.pk,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'token': str(token.key),
                        }
                        return Response({'success': True, 'message': 'Logged in Successfully', 'data': params},
                                        status=status.HTTP_200_OK)
                    else:
                        return Response({'success': False,
                                         'message': "Incorrect password. Try different or forgot password.",
                                         'data': None},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'success': False, 'message': "Both fields are required", 'data': None},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success': False, 'message': "Email/User not found. Try Signup", 'data': None},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': 'Something went wrong', 'data': None},
                            status=status.HTTP_400_BAD_REQUEST)


class GetData(APIView):
    def get(self, request):
        search = request.query_params.get('search', None)
        print("search", search)
        record_id = request.query_params.get('record_id', None)

        if search:
            try:
                search = int(search)
                qs = table1.objects.filter(permid__icontains=search)
                serializer = DataSerializers(qs, many=True)
                return Response({'success': True, 'message': '', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            except:
                qs = table1.objects.filter(name__icontains=search)
                serializer = DataSerializers(qs, many=True)
                return Response({'success': True, 'message': '', 'data': serializer.data},
                                status=status.HTTP_200_OK)
        elif record_id:
            qs = table1.objects.filter(id=int(record_id))
            if qs:
                serializer = DataSerializers(qs)
                return Response({'success': True, 'message': '', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': True, 'message': '', 'data': []},
                                status=status.HTTP_200_OK)
        else:
            qs = table1.objects.all().order_by('-lastmodifieddate')[0:10]
            serializer = DataSerializers(qs, many=True)
            return Response({'success': True, 'message': '', 'data': serializer.data},
                            status=status.HTTP_200_OK)

@login_required
def test(request):
    return render(request, "home.html")

def index(request):
    messages = ''
    if request.method == "POST":
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        print("email", email)
        print("password", password)
        user=authenticate(username= email, password= password)
        if user is not None:
            print("in if user")
            login(request, user)
            return redirect("home/")
        else:
            messages = "Invalid credentials! Please try again"
            print("in else user")
    return render(request, 'Login.html', {"messages": messages})

@login_required
def signout(request):
    logout(request)
    return render(request, 'Login.html', {"messages": ''})


@login_required(login_url="/")
def singleview(request, id):
    print("id", id)
    qs = table1.objects.filter(id=int(id)).first()
    if qs:
        serializer = DataSerializers(qs)
    return render(request, 'single.html', {"data":serializer.data})

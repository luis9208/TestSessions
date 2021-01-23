import re
from django.shortcuts import render

# Create your views here.
from .serializers import UserSerializer
from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.hashers import make_password


class CreateAuth(generics.CreateAPIView):
    
    def post(self, request):
        data = request.data
        pwd = make_password(request.data.get('password'))
        data.update({
            'password':pwd
        })
        serialized = UserSerializer(data=data)
        if serialized.is_valid():
            obj = serialized.save()
            obj.is_staff = True
            print(obj)
            obj.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Login(generics.CreateAPIView):
    def get(self, request):
        name = request.GET['name']
        if request.session.has_key('username'):
            username = request.session['username']
            if name == username:
                return Response(username)
            else:
                return Response({
                    'name':name,
                    'username':username
                })
        else:
            #retorna false cuando la session expira
            return Response(False)    
    
    def post(self, request):
        data = request.data
        form = AuthenticationForm(data=data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)
            if user is not None:
                # Hacemos el login manualmente          
                do_login(request, user)
                request.session['username'] = username
                request.session.set_expiry(120)
                request.session.modified = True
                return Response('logged')
            else:
                return Response('sin usuario')
        else:
            return Response('eroroes')
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Account
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.template import loader
from django.shortcuts import *
from django.core.files.storage import FileSystemStorage

class logout(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self,request):
        response = HttpResponseRedirect('/accounts/login/')
        response.delete_cookie('JWT')
        response.delete_cookie('user')
        return response

def akarsh(request):
    return render_to_response('index.html')

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response==None:
        return response

    if((response.status_code == 401) | (response.status_code == 403)):
        return redirect('/accounts/login/')
    else:
        return response

class RestrictedView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        data = {
            'id': request.user.id,
            'username': request.user.username,
            'token': str(request.auth)
        }
        return Response(data)

class AuthRegister(APIView):
    """
    Register a new user.
    """
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        if(request.data['faculty']=='False'):
            request.data['faculty'] = get_random_string(length=6)
            request.data['is_faculty'] = True
        else:
            request.data['is_faculty'] = False
        request.data['dp']=request.FILES['dp']
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class updateprofile(APIView):
    permission_classes = (IsAuthenticated,AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = AccountSerializer

    def get_object(self,request, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self,request):
        aka = self.get_object(request,request.user.id)
        rsh = loader.get_template('edit.html')
        cont = {
            'user': aka,
        }
        return HttpResponse(rsh.render(cont, request))

    def put(self, request):
        ala = self.get_object(request,request.user.id)
        # request.POST['email']=ala[0]['email']
        # request.POST['dp'] = ala[0]['dp']
        # request.POST['password'] = ala[0]['password']
        # request.POST['confirm_password'] = ala[0]['confirm_password']
        print (request.data)
        serializer = AccountSerializer(ala, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def red(request):
    return redirect('/accounts/login/')

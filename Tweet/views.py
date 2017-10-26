# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import posts,comments
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.template import loader
from django.shortcuts import *
from django.utils.decorators import method_decorator
from authentication.models import Account
from .forms import *
from rest_framework.response import Response
from rest_framework import status

class home(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @method_decorator(csrf_exempt)
    def get(self,request):
        tem = Account.objects.filter(id=request.user.id).values('faculty','is_faculty')
        aka = posts.objects.filter(user__faculty=tem[0]['faculty']).values('id','text','user__id','user__username')
        for post in aka:
            com=comments.objects.filter(post__id=post.id).values('id','text','user__id','user__username')
            post['comm']=com
        rsh = loader.get_template('newsfeed.html')
        cont = {
            'posts': aka,
            'user':request.user.id,
            'name':request.user.username,
            'is_fac':tem[0]['is_faculty'],
        }
        return HttpResponse(rsh.render(cont, request))

class timeline(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @method_decorator(csrf_exempt)
    def get(self,request,pk):
        if(pk==request.user.id):
            sel=True
        else:
            sel=False
        tem = Account.objects.filter(id=request.user.id).values('is_faculty')
        temw=Account.objects.filter(id=pk).values('username','is_faculty')
        aka = posts.objects.filter(comments__user__id=pk).values('id','text','user__id','user__username')
        for post in aka:
            com=comments.objects.filter(post__id=post.id).values('id','text','user__id','user__username')
            post['comm']=com
        rsh = loader.get_template('newsfeed.html')
        cont = {
            'posts': aka,
            'user': request.user.id,
            'name': request.user.username,
            'tuser':pk,
            'tname':temw[0]['name'],
            'tis_fac': temw[0]['is_faculty'],
            'is_fac': tem[0]['is_faculty'],
            'sele':sel,
        }
        return HttpResponse(rsh.render(cont, request))

class postview(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @method_decorator(csrf_exempt)
    def post(self,request):
        if not request.data._mutable:
            request.data._mutable = True
        request.data['user']=request.user.id
        ins=posts(request.POST)
        ins.save()
        return redirect('/tweet/home/')

class commview(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @method_decorator(csrf_exempt)
    def post(self,request,pk):
        if not request.data._mutable:
            request.data._mutable = True
        request.data['user']=request.user.id
        request.data['post'] = pk
        ins=comments(request.POST)
        ins.save()
        return redirect('/tweet/home/')
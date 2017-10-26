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
        tem = Account.objects.filter(id=request.user.id).values('faculty','is_faculty','dp')
        aka = posts.objects.filter(user__faculty=tem[0]['faculty']).values('id','text','user__id','user__username','pmedia','user__dp')
        for post in aka:
            comms=comments.objects.filter(post__id=post['id'])
            if(comms!={}):
                com=comms.values('id','text','user__id','user__username','user__dp')
                post['comment']=com
            else:
                post['comment'] = comms
            post['mtype']=post['pmedia'].split('.')[-1].lower()
        rsh = loader.get_template('newsfeed.html')
        cont = {
            'posts': aka,
            'user':request.user.id,
            'dp': tem[0]['dp'],
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
        tem = Account.objects.filter(id=request.user.id).values('is_faculty','dp')
        temw=Account.objects.filter(id=pk).values('username','is_faculty')
        aka = posts.objects.filter(comments__user__id=pk).values('id','text','user__id','user__username','pmedia','user__dp')
        for post in aka:
            com=comments.objects.filter(post__id=post['id']).values('id','text','user__id','user__username','user__dp')
            post['comment']=com
        rsh = loader.get_template('newsfeed.html')
        print(tem[0]['dp'])
        cont = {
            'posts': aka,
            'user': request.user.id,
            'name': request.user.username,
            'dp': tem[0]['dp'],
            'tuser':pk,
            'tname':temw[0]['username'],
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
        if not request.POST._mutable:
            request.POST._mutable = True
        request.POST['user']=request.user.id
        ins=postsForm(request.POST,request.FILES)
        if ins.is_valid():
            ins.save()
            return redirect('/tweet/home/')
        return HttpResponse(ins.errors)

class commview(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @method_decorator(csrf_exempt)
    def post(self,request,pk):
        if not request.POST._mutable:
            request.POST._mutable = True
        request.POST['user']=request.user.id
        request.POST['post'] = pk
        ins=commsForm(request.POST)
        if ins.is_valid():
            ins.save()
            return redirect('/tweet/home/')
        return HttpResponse(ins.errors)
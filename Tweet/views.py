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


class itemtodo(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self,request, pk):
        try:
            return ToDoItem.objects.filter(list=pk)
        except ToDoItem.DoesNotExist:
            raise Http404

    @method_decorator(csrf_exempt)
    def get(self,request,pk):
        if request.is_ajax():
            ak=ToDoList.objects.filter(user=request.user.id).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if pk in ak:
                aka=self.get_object(request,pk)
                serializer=ToDoItemSerializer(aka,many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect('/accounts/login/')


class itemnew(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @method_decorator(csrf_exempt)
    def post(self, request, pk):
        if request.is_ajax():
            ak=ToDoList.objects.filter(user=request.user).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if(pk in ak):
                if not request.data._mutable:
                    request.data._mutable = True
                request.data['list']=pk
                serializer = ToDoItemSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, safe=False)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("/accounts/login/")

class listupdate(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self,request, pk):
        try:
            return ToDoList.objects.get(pk=pk)
        except ToDoList.DoesNotExist:
            return Response(ToDoList.DoesNotExist, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_exempt)
    def get(self,request,pk):
        if request.is_ajax():
            ak = ToDoList.objects.filter(user=request.user).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if pk in ak:
                aka=self.get_object(request,pk)
                serializer = ToDoListSerializer(aka)
                return JsonResponse(serializer.data, safe=False)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("/accounts/login/")

    @method_decorator(csrf_exempt)
    def put(self,request,pk):
        if request.is_ajax():
            ak = ToDoList.objects.filter(user=request.user).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if pk in ak:
                ala=self.get_object(request,pk)
                if not request.data._mutable:
                    request.data._mutable = True
                #request.data.update({'user':request.user})
                request.data['user']=request.user.id
                serializer = ToDoListSerializer(ala, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, safe=False)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("/accounts/login/")

    @method_decorator(csrf_exempt)
    def delete(self,request,pk):
        if request.is_ajax():
            ak = ToDoList.objects.filter(user=request.user).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if pk in ak:
                aka=self.get_object(request,pk)
                aka.delete()
                return JsonResponse({"delete": True}, safe=False)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("/accounts/login/")

class itemupdate(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self,request, pk):
        try:
            return ToDoItem.objects.get(pk=pk)
        except ToDoItem.DoesNotExist:
            raise Http404

    @method_decorator(csrf_exempt)
    def get(self,request, pk):
        if request.is_ajax():
            ak = ToDoItem.objects.filter(list__user=request.user).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if pk in ak:
                aka = self.get_object(request,pk)
                serializer = ToDoItemSerializer(aka)
                return JsonResponse(serializer.data,safe=False)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("/accounts/login/")

    @method_decorator(csrf_exempt)
    def put(self, request, pk):
        if request.is_ajax():
            ak = ToDoItem.objects.filter(list__user=request.user).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if pk in ak:
                ala = self.get_object(request,pk)
                serializer = ToDoItemSerializer(ala, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, safe=False)
                print serializer.errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("/accounts/login/")

    @method_decorator(csrf_exempt)
    def delete(self,request,pk):
        if request.is_ajax():
            ak = ToDoItem.objects.filter(list__user=request.user).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if pk in ak:
                ala = self.get_object(request,pk)
                ala.delete()
                return JsonResponse({"delete":True}, safe=False)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("/accounts/login/")

class itemupd(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self,request, pk):
        try:
            return ToDoItem.objects.get(pk=pk)
        except ToDoItem.DoesNotExist:
            raise Http404

    @method_decorator(csrf_exempt)
    def get(self,request, pk):
        if request.is_ajax():
            ak = ToDoItem.objects.filter(list__user=request.user).values('pk')
            ak = [unicode(d['pk']) for d in ak]
            if pk in ak:
                aka = self.get_object(request,pk)
                serializer = ToDoItemSerializer(aka)
                ser_data=serializer.data
                ser_data['completed']=True
                serializer = ToDoItemSerializer(aka, data=ser_data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, safe=False)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'access':'access denied'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("/accounts/login/")
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
from django.utils.decorators import method_decorator
from .forms import *
import smtplib
from email.mime.text import MIMEText
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import posts,comments
from django.http import JsonResponse
from django.template import loader
from authentication.models import Account

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
        if(int(pk)==int(request.user.id)):
            sel=True
        else:
            sel=False
        tem = Account.objects.filter(id=request.user.id).values('is_faculty','dp')
        temw=Account.objects.filter(id=pk).values('username','is_faculty')
        aka = posts.objects.filter(comments__user__id=pk).values('id','text','user__id','user__username','pmedia','user__dp')
        for post in aka:
            com=comments.objects.filter(post__id=post['id']).values('id','text','user__id','user__username','user__dp')
            post['comment']=com
            post['mtype']=post['pmedia'].split('.')[-1].lower()
        rsh = loader.get_template('timeline.html')
        print(sel)
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

    def semail(self,request):
        usi=Account.objects.filter(id=request.user.id).values('faculty')
        tos=Account.objects.filter(faculty=usi[0]['faculty']).values('email','username','is_faculty')
        user = 'akarshc74@gmail.com'
        password = 'chinna030'
        fromm = user
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(user, password)
        for to in tos:
            if(to['is_faculty']==False):
                temp = loader.get_template('postsmtp.html')
                msg = MIMEText(temp.render({'user': to['username'], 'teacher': request.user.username}), 'html')
                # message = """From: """+fromm+"""
                # To: """+to['email']+"""
                # MIME-Version: 1.0
                # Content-type: text/html
                # Subject: You have new Notifications @TweetBook
                #
                # This is an e-mail message to be sent in HTML format. """+msg.as_string()
                # subject='You have new Notifications @TweetBook'
                # bod='Subject: {}\n\n{}'.format(subject, msg.as_string())
                server.sendmail(fromm, to['email'], msg.as_string())
        server.quit()

    @method_decorator(csrf_exempt)
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable = True
        request.POST['user']=request.user.id
        ins=postsForm(request.POST,request.FILES)
        if ins.is_valid():
            ins.save()
            self.semail(request)
            return redirect('/tweet/home/')
        return HttpResponse(ins.errors)

class commview(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def semail(self,request,pk):
        usi=posts.objects.filter(id=pk).values('user__email','user__username')
        user = 'akarshc74@gmail.com'
        password = 'chinna030'
        fromm = user
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(user, password)
        temp = loader.get_template('commsmtp.html')
        msg = MIMEText(temp.render({'user': usi['user__username'], 'teacher': request.user.username}), 'html')
        # message = """From: """+fromm+"""
        # To: """+usi['user__email']+"""
        # MIME-Version: 1.0
        # Content-type: text/html
        # Subject: You have new Notifications @TweetBook
        #
        # This is an e-mail message to be sent in HTML format. """+msg.as_string()
        # subject='You have new Notifications @TweetBook'
        # bod='Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(fromm, usi['user__email'], msg.as_string())
        server.quit()

    @method_decorator(csrf_exempt)
    def post(self,request,pk):
        if not request.POST._mutable:
            request.POST._mutable = True
        request.POST['user']=request.user.id
        request.POST['post'] = pk
        ins=commsForm(request.POST)
        if ins.is_valid():
            ins.save()
            self.semail(request,pk)
            return redirect('/tweet/home/')
        return HttpResponse(ins.errors)
import json

import requests
from allauth.account.views import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import resolve
from django.urls import reverse
from rest_framework.response import Response


# @login_required
def login_view(request):
    if request.method == 'POST':
        # POST 요청으로 넘겨받은 아이디/패스워드로 토큰을 받아온다.
        # data = {
        #     'username': request.POST['username'],
        #     'password': request.POST['password']
        # }
        # url = 'http://localhost:8000/api/member/token-auth/'
        # response = requests.post(url, data=data)
        # response_json = response.json()
        print('login')
        login(request)

        return render(request, 'member/success.html')
    return render(request, 'member/login.html')

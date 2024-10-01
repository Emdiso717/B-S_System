from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
@csrf_exempt
def login(request):
        data = json.loads(request.body)
        account = data.get('account')
        password = data.get('password')
        return HttpResponse("success")


@csrf_exempt
def register(request):
        data = json.loads(request.body)

        return HttpResponse("success")
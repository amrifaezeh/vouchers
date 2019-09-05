from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Voucher

def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render(None, request))

# Create your views here.

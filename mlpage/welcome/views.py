# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader
from django.http import HttpResponse

# Create your views here.
def index(request):
    template = loader.get_template('Home/Index.html')
    return HttpResponse(template.render())

def home(request):
    template = loader.get_template('Home/HomePage.html')
    return HttpResponse(template.render())

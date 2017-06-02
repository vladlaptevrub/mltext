# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader
from django.http import HttpResponse

# Create your views here.
def py_index(request):
    template = loader.get_template('Python/HelloWorld.html')
    return HttpResponse(template.render())

def hello(request):
    template = loader.get_template('Python/HelloWorld.html')
    return HttpResponse(template.render())

def introduction(request):
    template = loader.get_template('Python/Introduction.html')
    return HttpResponse(template.render())

def pandas(request):
    template = loader.get_template('Python/Pandas.html')
    return HttpResponse(template.render())

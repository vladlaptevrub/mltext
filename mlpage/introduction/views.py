# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader
from django.http import HttpResponse

# Create your views here.
def ml_index(request):
    template = loader.get_template('Introduction/MachineLearning.html')
    return HttpResponse(template.render())

def ml(request):
    template = loader.get_template('Introduction/MachineLearning.html')
    return HttpResponse(template.render())

def problems(request):
    template = loader.get_template('Introduction/Problems.html')
    return HttpResponse(template.render())

def tasks(request):
    template = loader.get_template('Introduction/Tasks.html')
    return HttpResponse(template.render())

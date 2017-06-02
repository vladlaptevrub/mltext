# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def pc_index(request):
    start_string = 'print ("Hello, World!")'
    return render(request, 'Compiler/CompilerView.html', {'start_string': start_string})

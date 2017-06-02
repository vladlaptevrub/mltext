# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import pandas
from time import time
from django.conf import settings
import os
from naive_b.models import TestData
from naive_b.models import Classifier
from naive_b.models import Results
from naive_b import classifier

# Create your views here.
def nb_index(request, id):
    template = loader.get_template('NaiveB/Dataset.html')
    return HttpResponse(template.render())

def dataset(request):
    template = loader.get_template('NaiveB/Dataset.html')
    return HttpResponse(template.render())

def tokenization(request):
    template = loader.get_template('NaiveB/Tokenization.html')
    return HttpResponse(template.render())

def normalization(request):
    template = loader.get_template('NaiveB/Normalization.html')
    return HttpResponse(template.render())

def features(request):
    template = loader.get_template('NaiveB/Features.html')
    return HttpResponse(template.render())

def classifiers(request):
    template = loader.get_template('NaiveB/Classifiers.html')
    return HttpResponse(template.render())

@csrf_exempt
def result(request):
    template = loader.get_template('NaiveB/Result.html')
    return HttpResponse(template.render())

@csrf_exempt
def test(request):
    if request.method == 'POST':
        sw_string = request.POST['stop_words']
        sym_string = request.POST['symbols']
        nf_string = request.POST['norm_form']
        class_name_string = request.POST['class_name']

        Classifier.objects.create(
            class_id=class_name_string,
            stopw=sw_string,
            symb=sym_string,
            normal=nf_string,
        )

        return HttpResponse(request)

@csrf_exempt
def test_get(request):
    sw = ["что", "как", "такое", "это", "этот", "за", "в", "к", "какой", "же"]

    sym = [",", ".", "!", "?"]

    #fb = open('dataset.csv', encoding='utf-8')
    fb = open(os.path.join(settings.PROJECT_ROOT, 'dataset.csv'), encoding='utf-8')
    csv_data_b = pandas.read_csv(fb, sep=',', skiprows=[0], header=None)

    my_list_text_new = []
    my_list_types_new = []
    i = 10000

    if request.method == "GET":
        count = 0
        is_sw = 0
        is_sym = 0
        is_norm = 0

        #while i < 10100:
            #item = csv_data_b[0][i]
            #type = csv_data_b[1][i]
            #my_list_text_new.append(item)
            #my_list_types_new.append(type)
            #i += 1

        # READ DATA FROM DB
        databasetest = TestData.objects.all()
        for data in databasetest:
            my_list_text_new.append(data.text)
            my_list_types_new.append(data.label)
            count += 1

        # READ PROPERTIES FROM DB
        classData = Classifier.objects.all().order_by('-id')[:1]

        for cdata in classData:
            sw_string = cdata.stopw
            if (len(sw_string) > 1):
                if (isinstance(sw_string, str)):
                    stopw = sw_string.split(', ')
                    is_sw = 1
                    print("STOP WORDS:", stopw)

            if (is_sw == 0):
                stopw = []

            sym_string = cdata.symb
            if (len(sym_string) > 1):
                if (isinstance(sym_string, str)):
                    symbols = sym_string.split(', ')
                    is_sym = 1
                    print("SYMBOLS:", symbols)

            if (is_sym == 0):
                symbols = []

            class_name = cdata.class_id
            norm = cdata.normal

        if (norm == 'true'):
            is_norm = 1

        # START CLASSIFY TEXT DATA
        tic = time()
        res = classifier.classify(is_sw, stopw, is_sym, symbols, is_norm, my_list_text_new, my_list_types_new, class_name)
        toc = time()

        # CHECK TIME OF WORK
        print("Time:", toc - tic)

        # ADD RESULTS TO DB
        Results.objects.create(
            score=res/count*100,
            goods=res,
            bads=count-res,
            properties_id=0
        )

        return HttpResponse(res/count*100)

@csrf_exempt
def post_test_data(request):
    if request.method == 'POST':
        test_string = request.POST['string']
        test_label = request.POST['label']

        TestData.objects.create(
            text=test_string,
            label=test_label,
        )

        return HttpResponse(request)

@csrf_exempt
def delete_test_data(request):
    if request.method == 'POST':
        action = request.POST['action']

        if (action == 'delete'):
            TestData.objects.all().delete()

        return HttpResponse(request)

@csrf_exempt
def delete_class_data(request):
    if request.method == 'POST':
        action = request.POST['action']

        if (action == 'delete'):
            Classifier.objects.all().delete()

        return HttpResponse(request)

@csrf_exempt
def get_history(request):
    if request.method == 'GET':
        res = Results.objects.all().order_by('-id')[:1]
        res_json = serializers.serialize('json', res)
        return HttpResponse(res_json, content_type='application/json')
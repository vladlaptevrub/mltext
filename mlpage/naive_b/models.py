# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



class User(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)


class Classifier(models.Model):
    class_id = models.CharField(max_length=64)
    stopw = models.CharField(max_length=1024)
    symb = models.CharField(max_length=512)
    normal = models.CharField(max_length=64)

class TestData(models.Model):
    text = models.CharField(max_length=1024)
    label = models.CharField(max_length=64)

class Results(models.Model):
    score = models.DecimalField(max_digits=14, decimal_places=10)
    goods = models.IntegerField()
    bads = models.IntegerField()
    properties_id = models.IntegerField()
# -*- coding: utf-8 -*-

from django.db import models


class CDNFile(models.Model):
    package = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    url = models.CharField(max_length=511)
    version = models.CharField(max_length=16)

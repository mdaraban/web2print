#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Product
        exclude = ['slug']
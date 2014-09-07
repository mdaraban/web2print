#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('product_format.backend_views',
    url(r'^admin/product-format/form/(?P<pk>.*)', 'form', name="admin-product-format-form"),
    url(r'^admin/product-format/form', 'form', name="admin-product-format-form"),
    url(r'^admin/product-format/details/(?P<pk>.*)', 'details', name="admin-product-format-details"),
    url(r'^admin/product-format/delete/(?P<pk>.*)', 'delete', name="admin-product-format-delete"),
    url(r'^admin/product-format/list', 'list', name="admin-product-format-list"),
    url(r'^admin/product-format', 'index', name="admin-product-format-index"),
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy, reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.context_processors import csrf

from .models import PrintingPrice
from .forms import PrintingPriceForm

context = {'page_title': "Cijene printa"}

@login_required()
@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy("admin-login"))
def index(request):
    return HttpResponseRedirect(reverse("admin-printing-price-list"))


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy("admin-login"))
def list(request):
    order_by = request.GET.get("order_by")
    order_type = request.GET.get("order_type")
    rows_list = PrintingPrice.objects.all()

    if order_by:
        if order_type == "asc":
            order = order_by
        else:
            order = "-" + order_by
        rows_list = rows_list.order_by(order)

    paginator = Paginator(rows_list, settings.RESULTS_PER_PAGE)

    page = request.GET.get('page')
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rows = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        rows = paginator.page(paginator.num_pages)

    context["rows"] = rows
    return render_to_response('backend/printing_price/list.html', context, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy("admin-login"))
def form(request, pk=None):

    printing_price_id = request.GET.get("printing_price_id", None)
    initial = {}
    if printing_price_id:
        initial = PrintingPrice.objects.filter(pk=printing_price_id).values()[0]
        initial["printer"] = initial["printer_id"]

    if request.POST:
        if pk:
            object = PrintingPrice.objects.get(pk=pk)
            form = PrintingPriceForm(request.POST, instance=object)
        else:
            form = PrintingPriceForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("admin-printing-price-list"))
    else:
        if pk:
            object = PrintingPrice.objects.get(pk=pk)
            form = PrintingPriceForm(instance=object)
        else:
            form = PrintingPriceForm(initial=initial)

    context.update(csrf(request))

    context['form'] = form

    return render_to_response('backend/printing_price/form.html', context, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy("admin-login"))
def details(request, pk):
    row = PrintingPrice.objects.get(pk=pk)
    context['row'] = row

    return render_to_response('backend/printing_price/details.html', context, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy("admin-login"))
def delete(request, pk):
    entry = PrintingPrice.objects.get(pk=pk)
    entry.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.utils.encoding import smart_text
from django import template
from django import forms
from django.utils.datastructures import SortedDict

from web2print.settings.base import APPLICATION_NAME, APPLICATION_VERSION

register = template.Library()


def get_fieldset(parser, token):
    try:
        name, fields, as_, variable_name, from_, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r' % token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form)

get_fieldset = register.tag(get_fieldset)


class FieldSetNode(template.Node):
    def __init__(self, fields, variable_name, form_variable):
        self.fields = fields
        self.variable_name = variable_name
        self.form_variable = form_variable

    def render(self, context):

        form = template.Variable(self.form_variable).resolve(context)
        new_form = copy.copy(form)
        new_form.fields = SortedDict([(key, value) for key, value in form.fields.items() if key in self.fields])

        context[self.variable_name] = new_form

        return u''

def th(context, label, name=None, width=None, css_class=None):

    request = context.get('request')
    request_dict = request.GET.copy()
    label = smart_text(label)

    return_string = "<th"
    if width:
        return_string += " width='" + width + "%'"

    if css_class:
        return_string += " class='" + css_class + "'"

    if name:
        a_css_class = None
        if "order_by" in request_dict.keys() and request_dict["order_by"] == name:
            if request_dict["order_type"] == "asc":
                request_dict["order_type"] = "desc"
                a_css_class = "asc"
            else:
                request_dict["order_type"] = "asc"
                a_css_class = "desc"
        else:
            request_dict["order_by"] = name
            request_dict["order_type"] = "asc"

        return_string += "><a "
        if a_css_class:
            return_string += "class='" + a_css_class + "' "
        return_string += "href='?" + request_dict.urlencode() + "' title='" + label + "'><b></b>" + label + "</a></th>"
    else:
        return_string += "><span>" + label + "</span></th>"

    return return_string
register.simple_tag(takes_context=True)(th)


def th_operation(css_class=None):
    if css_class:
        return "<th width='10%' class='" + css_class + "'><span>Operacije</span></th>"
    else:
        return "<th width='10%'><span>Operacije</span></th>"
register.simple_tag()(th_operation)


def td(context, label, name=None, css_class=None):

    request = context.get('request')
    request_dict = request.GET.copy()
    label = smart_text(label)

    return_string = "<td "

    if name:
        a_css_class = None
        if "order_by" in request_dict.keys() and request_dict["order_by"] == name:
            a_css_class = "sorted"

        if a_css_class:
            if css_class:
                css_class+= " " + a_css_class
            else:
                css_class = a_css_class

    if css_class:
        return_string+= "class='" + css_class + "'"

    return_string += ">" + label + "</td>"

    return return_string
register.simple_tag(takes_context=True)(td)


def button_new(label, link):
    return "<a class='button new' href='" + reverse(link) + "'>" + label + "</a>"
register.simple_tag(button_new)


def application_name():
    return APPLICATION_NAME
register.simple_tag(application_name)


def application_version():
    return APPLICATION_VERSION
register.simple_tag(application_version)


def h1(label):
    return "<h1>" + label + "</h1>"
register.simple_tag(h1)


def h2(label):
    return "<h2>" + label + "</h2>"
register.simple_tag(h2)


def h3(label):
    return "<h3>" + label + "</h3>"
register.simple_tag(h3)


def h4(label):
    return "<h4>" + label + "</h4>"
register.simple_tag(h4)


def current_datetime(format, days_to_add = None):
    current_datetime = datetime.now()
    if days_to_add:
        current_datetime = current_datetime + timedelta(days=days_to_add)
    return current_datetime.strftime(format)

register.simple_tag(current_datetime)


def pager(context, rows):

    request = context.get('request')
    request_dict = request.GET.copy()

    return_string = ""
    if rows:
        return_string += "<div class='pager'><div class='pages'>"
        if rows.paginator.page_range < 10:
            for x in rows.paginator.page_range:
                request_dict["page"] = x
                if rows.number == x:
                    return_string += "<a href='?" + request_dict.urlencode() + "' class='current'>" + str(x) + "</a>"
                else:
                    return_string += "<a href='?" + request_dict.urlencode() + "'>" + str(x) + "</a>"
        else:
            number_of_pages = len(rows.paginator.page_range)
            for x in rows.paginator.page_range:
                request_dict["page"] = x

                if (x < 6 or x > (number_of_pages-5)) or \
                        (rows.number-5 < x and rows.number+5 > x):
                    if rows.number == x:
                        return_string += "<a href='?" + request_dict.urlencode() + "' class='current'>" + str(x) + "</a>"
                    else:
                        return_string += "<a href='?" + request_dict.urlencode() + "'>" + str(x) + "</a>"
                elif (x is 6 and rows.number-4 > 6) or (x == (number_of_pages-5) and rows.number+4 < number_of_pages-4):
                    return_string += "<span>...</span>"

        return_string += "</div></div>"

    return return_string

register.simple_tag(takes_context=True)(pager)


def is_in_group(context, group):
    if lambda u: u.groups.filter(name=group).count() == 1:
        return True
    else:
        return False

register.simple_tag(takes_context=True)(is_in_group)

def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()
register.simple_tag(get_verbose_field_name)
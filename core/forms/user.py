#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = self.instance.pk is None
        if self.instance.pk:
            self.fields['password'].label = "Nova lozinka"
        else:
            self.fields['password'].label = "Lozinka"

        self.fields['username'].label = "Korisničko ime"
        self.fields['is_superuser'].label = "Administrator"
        self.fields['is_active'].label = "Aktivan"

    class Meta:
        model = User
        exclude = ('last_login', 'date_joined', 'reset_password_code_expiration', 'reset_password_code',
                   'activation_code')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if user.pk:
            if password:
                user.set_password(self.cleaned_data["password"])
            else:
                existing_user = User.objects.get(pk=user.pk)
                user.password = existing_user.password
        else:
            user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
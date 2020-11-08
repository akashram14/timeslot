from django import forms
from django.db import models
from .models import Orders

class choosetime(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'

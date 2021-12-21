from django import forms
from django.db.models import fields
from django import forms
from .models import FormMain
from django.forms import ModelForm

class FormmainForm(ModelForm):
    class Meta:
        model = FormMain
        exclude = ['usethisbool','createdby']
from django import forms
from django.forms import Textarea, TextInput, DateTimeField, DateInput, DateField
from django.forms.widgets import SelectDateWidget
from datetime import datetime, time
from .models import article
from django.contrib.admin.widgets import AdminDateWidget



class ArticleSearch(forms.ModelForm):
    class Meta:
        model = article
        labels = {
            "abstract": " ",

        }

        fields = ['abstract']
        widgets = {
            'abstract': TextInput(attrs={'size':'42','placeholder':"Surf on Covid-19 Articles", "class":"form-control", "style":"font-family:Times New Roman;width:98%"}),


        }





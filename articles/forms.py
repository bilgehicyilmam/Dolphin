from django import forms
from django.forms import Textarea, TextInput, DateTimeField, DateInput
from datetime import datetime, time
from .models import article

#class ArticleForm(forms.ModelForm):
#    class Meta:
#        model = article
#        fields = ['pubmed_id', 'id', 'title', 'abstract', 'keywords', 'journal', 'publication_date', 'authors', 'conclusions', 'results', 'copyrights', 'doi']

class ArticleSearch(forms.ModelForm):
    class Meta:
        model = article
        labels = {
            "abstract": " ",
            "publication_date": "Faceted Search"
        }

        fields = ['abstract']
        widgets = {
            'abstract': TextInput(attrs={'size':'70','placeholder':"Surf on Covid-19 Articles", "class":"form-control", "style":"font-family:Times New Roman"})
            #'publication_date': datetime(attrs={'input_formats': ["%Y-%m-%d %H:%M:%S"]}),
            #'publication_date' : forms.DateTimeField(required=False,input_formats=['%Y-%m-%d %H:%M:%S'])

        }
        #publication_date = DateTimeField(required=False,input_formats=['%Y-%m-%d %H:%M:%S'])
        #publication_date = forms.DateField(widget=DateInput)
#class DateInput(forms.DateInput):
    #input_type = 'date'



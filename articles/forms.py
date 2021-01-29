from django import forms
from django.forms import Textarea, TextInput, DateTimeField, DateInput, DateField
from django.forms.widgets import SelectDateWidget
from datetime import datetime, time
from .models import article
from django.contrib.admin.widgets import AdminDateWidget

#class ArticleForm(forms.ModelForm):
#    class Meta:
#        model = article
#        fields = ['pubmed_id', 'id', 'title', 'abstract', 'keywords', 'journal', 'publication_date', 'authors', 'conclusions', 'results', 'copyrights', 'doi']

class ArticleSearch(forms.ModelForm):
    class Meta:
        model = article
        labels = {
            "abstract": " ",
            #"publication_date": ""
        }

        fields = ['abstract']
        widgets = {
            'abstract': TextInput(attrs={'size':'70','placeholder':"Surf on Covid-19 Articles", "class":"form-control", "style":"font-family:Times New Roman"}),
            #'publication_date': forms.SelectDateWidget(years=range(1900,2022))
            #'publication_date': forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),)
            #'publication_date': forms.SelectDateWidget(
            #'publication_date': forms.DateField(widget=AdminDateWidget())
            #'publication_date': forms.DateField(widget=forms.TextInput(attrs= { 'class':'datepicker' }))
            #'publication_date': forms.DateTimeField(required=False, input_formats=['%Y-%m-%d %H:%M:%S'])

        }
        #publication_date = DateTimeField(required=False,input_formats=['%Y-%m-%d %H:%M:%S'])
        #publication_date = forms.DateField(widget=DateInput)
#class DateInput(forms.DateInput):
    #input_type = 'date'

# class DateRangeForm(forms.Form):
#   def __init__(self, *args, **kwargs):
#     initial_start_date = kwargs.pop('initial_start_date')
#     initial_end_date = kwargs.pop('initial_end_date')
#     required_val = kwargs.pop('required')
#
#     super(DateRangeForm,self).__init__(*args,**kwargs)
#     self.fields['start_date'].initial = initial_start_date
#     self.fields['start_date'].required = required_val
#     self.fields['end_date'].initial = initial_end_date
#     self.fields['end_date'].required = required_val
#
#   start_date = forms.DateField()
#   end_date = forms.DateField()



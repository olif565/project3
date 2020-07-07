from django import forms
from django.forms import TextInput

from .models import Data
from .models import DataTesting


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['no', 'ppm_ch4', 'ppm_c2h4', 'ppm_c2h2', 'fault']


class DataTestingForm(forms.ModelForm):
    class Meta:
        model = DataTesting
        fields = ['no', 'ppm_ch4', 'ppm_c2h4', 'ppm_c2h2', 'fault']


class NormalisasiForm(forms.Form):
    sigma = forms.CharField(label='Sigma', required=True, max_length=100,
                            widget=TextInput(attrs={'type': 'number'}),
                            error_messages={'required': "Sigma"})


class ParameterForm(forms.Form):
    lamda = forms.CharField(label='Lambda', required=True, max_length=100,
                             widget=TextInput(attrs={'type': 'number'}),
                             error_messages={'required': "Lambda"})
    complexity = forms.CharField(label='Complexity', required=True, max_length=100,
                                widget=TextInput(attrs={'type': 'number'}),
                                error_messages={'required': "Constant"})
    gamma = forms.CharField(label='Gamma', required=True, max_length=100,
                             widget=TextInput(attrs={'type': 'number'}),
                             error_messages={'required': "Gamma"})
    iterasi = forms.CharField(label='Iterasi', required=True, max_length=100,
                               widget=TextInput(attrs={'type': 'number'}),
                               error_messages={'required': "Iterasi"})


class ParameterFormKfold(forms.Form):
    lamda = forms.CharField(label='Lambda', required=True, max_length=100,
                             widget=TextInput(attrs={'type': 'number'}),
                             error_messages={'required': "Lambda"})
    complexity = forms.CharField(label='Complexity', required=True, max_length=100,
                                widget=TextInput(attrs={'type': 'number'}),
                                error_messages={'required': "Complexity"})
    gamma = forms.CharField(label='Gamma', required=True, max_length=100,
                             widget=TextInput(attrs={'type': 'number'}),
                             error_messages={'required': "Gamma"})
    iterasi = forms.CharField(label='Iterasi', required=True, max_length=100,
                               widget=TextInput(attrs={'type': 'number'}),
                               error_messages={'required': "Iterasi"})
    split = forms.CharField(label='K-fold', required=True, max_length=100,
                              widget=TextInput(attrs={'type': 'number'}),
                              error_messages={'required': "Split"})



from django import forms

class FilterForm(forms.Form):

    min = forms.DecimalField(max_digits=20, decimal_places=2)
    max = forms.DecimalField(max_digits=20, decimal_places=2)
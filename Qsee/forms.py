from django import forms
from .models import cid
from .models import westgard

class TestInputForm(forms.Form):
    """Control and Analyser ID returned from test_input in view.py"""
    control_id = forms.IntegerField(validators=[cid]) #(widget=forms.HiddenInput(), required=False, validators=[westgard])
    result = forms.FloatField(min_value=0.0, max_value=45.0, validators=[westgard])
    test_date = forms.CharField(required=False)
    operator = forms.CharField()
    note = forms.CharField(required=False)

class AssayForm(forms.Form):
    assay = forms.CharField()

class ControlForm(forms.Form):
    assay_id = forms.IntegerField()
    control_name = forms.CharField()
    lot_number = forms.CharField()
    date_added = forms.CharField()
    active = forms.BooleanField(required=True)

class AnalyserForm(forms.Form):
    analyser = forms.CharField()
from django import forms
from .models import cid, westgard, datecheck

class TestInputForm(forms.Form):
    """Control and Analyser ID returned from test_input in view.py"""
    control_id = forms.IntegerField(validators=[cid], widget=forms.HiddenInput(), required=False)
    # Set user min and max has this is the number of cycles the PCR runs for
    result = forms.FloatField(min_value=0.0, max_value=45.0, validators=[westgard])
    # add a widget to ensure that the date is entered correctly
    test_date = forms.CharField(required=False, validators=[datecheck])
    operator = forms.CharField()
    # note field is not required
    note = forms.CharField(required=False)


class AssayForm(forms.Form):
    assay = forms.CharField()


class ControlForm(forms.Form):
    assay_id = forms.IntegerField()
    control_name = forms.CharField()
    lot_number = forms.CharField()
    # add a widget to ensure that the date is entered correctly
    date_added = forms.DateField(widget=forms.SelectDateWidget())
    # not required as control maybe received but not used yet
    active = forms.BooleanField(required=False)


class AnalyserForm(forms.Form):
    analyser = forms.CharField()
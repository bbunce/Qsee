from django import forms

class TestInputForm(forms.Form):
    """Control and Analyser ID returned from test_input in view.py"""
    result = forms.FloatField(min_value=0.0, max_value=45.0)
    test_date = forms.DateTimeField(required=False)
    operator = forms.CharField()
    note = forms.CharField(required=False)

class AssayForm(forms.Form):
    assay = forms.CharField()

class ControlForm(forms.Form):
    assay_id = forms.IntegerField()
    control_name = forms.CharField()
    lot_number = forms.CharField()
    date_added = forms.DateField()
    active = forms.BooleanField(required=False)

class AnalyserForm(forms.Form):
    analyser = forms.CharField()
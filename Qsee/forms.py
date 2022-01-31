from django import forms

class TestInputForm(forms.Form):
    result = forms.FloatField(label="Control result")
    test_date = forms.CharField(max_length=50)
    control_id = forms.IntegerField()
    analyser_id = forms.IntegerField()
    operator = forms.CharField(max_length=50)
    note = forms.CharField(max_length=200, required=False)

class AnalyserForm(forms.Form):
    analyser = forms.CharField(max_length=200)
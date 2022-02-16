from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Assay, Control, Analyser, Test, MR_ControlChart, stdev
from .forms import TestInputForm, AssayForm, ControlForm, AnalyserForm
import numpy as np
import pandas as pd
import math


# Create your views here.
def index(request):
    """Returns Qsee homepage"""
    return render(request, 'Qsee/index.html')

def assays(request):
    """Returns page that displays all available assays"""
    # database query that returns all the objects in the Assay table
    # SQL: SELECT * FROM assay;
    assays = Assay.objects.all()
    # return assay.html webpage and pass the results from the database query
    return render(request, 'Qsee/assays.html', {'assays': assays})

def controls(request, assay_id):
    """Returns page that displays all controls associated with the previously selected assay"""
    # error handling to manage users changing the assay id in the url for a record that does not exist
    # Return 404 error with a custom message if the assay or control does not exist.
    try:
        assay = Assay.objects.get(pk=assay_id)
    except Exception as e:
        print(e)
        raise Http404("Assay does not exist. Add assays in Settings.")
    try:
        controls = Control.objects.filter(assay_id=assay_id)
    except Exception as e:
        print(e)
        raise Http404(f"No controls exist for {assay.assay_name}")

    return render(request, 'Qsee/controls.html', {'assay': assay, 'controls': controls})

def qsee_error(request):
    """Displays error page that includes nav bar and option to contact administrator for support on
    the event of an error occuring"""
    return render(request, 'Qsee/404Error.html')

def result_menu(control_id):

    values = list(Test.objects.filter(control_id = control_id).order_by('id').values_list('result', flat=True))
    print(values)
    #values = [float(i) for i in values]  # Converts all values in list to floats
    values2 = np.array(values)
    dates = list(Test.objects.filter(control_id = control_id).order_by('id').values_list('test_date', flat=True))
    print(dates)
    dates2 = np.array(dates)
    total = 0
    # Require at least 20 QC entries before any kind of analysis can be made.
    if len(values) < 20:
        print("There are not enough QC entries to formulate an accurate Westgard plot. Currently: " + str(len(values)))
        print("You require at least 20 to begin.")
    else:
        # Takes all QC values in list to generate a global COV and SD figure
        onesd = stdev(values)
        for i in values:
            total += i
        average = total / len(values)
        cov = (onesd / average) * 100
        # Send array of control values to QC chart
        chart = MR_ControlChart()
        chart.fit(values2, dates2)
        chart.ControlChart(d2=1.128, D3=0, D4=3.267, onesd=onesd, average=average, cov=cov)  # Random values for now. Requires assignment for mR chart.

def tests(request, control_id):
    """Displays all the results for the control separated by the analyser they were used on"""
    analysers = Analyser.objects.all()
    control= Control.objects.get(id=control_id)
    # get a unique list of analysers this control has been used on
    analyser_ids = set([id.analyser_id for id in list(Test.objects.filter(control_id = control_id))])
    # create a dict with keys=analyser, values=test data for control used on said analyser
    tests_analyser = {}
    for analyser in analyser_ids:
        tests_analyser[analyser] = Test.objects.filter(control_id=control_id, analyser_id=analyser)

    result_menu(control_id)
    return render(request, 'Qsee/tests.html', {'control': control, 'tests_analyser': tests_analyser, 'analysers': analysers})

def settings(request):
    """Displays available assays, control and analysers. Each section has a form so that new items for
    each category can be added by the user"""
    assays = Assay.objects.all()
    controls = Control.objects.all()
    analysers = Analyser.objects.all()
    assay_form = AssayForm()
    control_form = ControlForm()
    analyser_form = AnalyserForm()
    return render(request, 'Qsee/settings.html', {"assays": assays,
                                                "controls": controls,
                                                "analysers": analysers,
                                                "assay_form": assay_form,
                                                "control_form": control_form,
                                                "analyser_form": analyser_form})

def settings_assay(request):
    """Adds new assay to the database"""
    form = AssayForm()
    # check to see if the the request method is POST
    if request.method == "POST":
        # if true then create an object containing the AssayForm details
        form = AssayForm(request.POST)
        if form.is_valid():
            # if the contents of the form is correct retrieve data from form
            assay = form.cleaned_data["assay"]
            # create a new assay object with the new assay name
            add_assay = Assay(assay_name=assay)
            # save assay objec to the database
            add_assay.save()
            # return user to the settings page
            return HttpResponseRedirect('/settings/')
    # if an error occurs go to qsee_error page
    return render(request, 'Qsee/404Error.html')


def settings_control(request):
    """Adds new control to the database"""
    form = ControlForm()
    if request.method == "POST":
        form = ControlForm(request.POST)
        if form.is_valid():
            assay_id = Assay.objects.get(pk=form.cleaned_data['assay_id'])
            control_name = form.cleaned_data["control_name"]
            lot_number = form.cleaned_data["lot_number"]
            # date_added = form.cleaned_data["date_added"]
            active = form.cleaned_data["active"]
            add_control = Control(assay_id=assay_id, control_name=control_name,
                                lot_number=lot_number, date_added=date_added, active=active)
            add_control.save()
            return HttpResponseRedirect('/settings/')
    # if an error occurs go to qsee_error page
    return render(request, 'Qsee/404Error.html')


def settings_analyser(request):
    """Adds new Analyser to the database"""
    form = AnalyserForm()
    if request.method == "POST":
        form = AnalyserForm(request.POST)
        if form.is_valid():
            analyser = form.cleaned_data["analyser"]
            add_analyser = Analyser(analyser_name=analyser)
            add_analyser.save()
            return HttpResponseRedirect('/settings/')
    # if an error occurs go to qsee_error page
    return render(request, 'Qsee/404Error.html')


def test_input(request, control_id, analyser_id):
    """Form to allow user to add a control result to the Qsee database"""
    ctrl = Control.objects.get(pk=control_id)
    # get control and analyser details from the url to so that the user can check that they are
    # entering the results for the correct control on the correct analyser.
    control_details = f"{ctrl.assay_id} {ctrl.control_name}"
    analyser_details = Analyser.objects.get(pk=analyser_id).analyser_name
    form = TestInputForm({'control_id': control_id})
    if request.method == "POST":
        form = TestInputForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data["result"]
            date = form.cleaned_data["test_date"]
            control = control_id
            analyser = analyser_id
            operator = form.cleaned_data["operator"]
            note = form.cleaned_data["note"]
            test = Test(result=result, test_date=date, control_id=Control.objects.get(pk=control), \
                        analyser_id=Analyser.objects.get(pk=analyser), operator=operator, note=note)
            test.save()
            return HttpResponseRedirect(f'/tests/{control}')
    return render(request, 'Qsee/test_input.html', {"form": form, "control_details": control_details, "analyser_details": analyser_details, 'control_id': control_id})

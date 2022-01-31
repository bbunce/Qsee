from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, get_list_or_404
from .models import Assay, Control, Analyser, Test
from .forms import TestInputForm, AnalyserForm

# Create your views here.
def index(request):
    return render(request, 'Qsee/index.html')

def assays(request):
    assays = Assay.objects.all()
    return render(request, 'Qsee/assays.html', {'assays': assays})

def controls(request, assay_id):
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

def analysers(request):
    return render(request, 'Qsee/index.html')

def tests(request, control_id):
    control= Control.objects.get(id=control_id)
    # get a unique list of analysers this control has been used on
    analyser_ids = set([id.analyser_id for id in list(Test.objects.filter(control_id = control_id))])
    # create a dict with keys=analyser, values=test data for control used on said analyser
    tests_analyser = {}
    for analyser in analyser_ids:
        tests_analyser[analyser] = Test.objects.filter(control_id=control_id, analyser_id=analyser)

    return render(request, 'Qsee/tests.html', {'control': control, 'tests_analyser': tests_analyser})

def settings(request):
    form = AnalyserForm()
    if request.method == "POST":
        form = AnalyserForm(request.POST)
        if form.is_valid():
            analyser = form.cleaned_data["analyser"]
            print("Analyser:", analyser)
            add_analyser = Analyser(analyser_name=analyser)
            add_analyser.save()
    return render(request, 'Qsee/settings.html', {"form": form})

def test_input(request):
    form = TestInputForm()
    if request.method == "POST":
        form = TestInputForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data["result"]
            date = form.cleaned_data["test_date"]
            control = form.cleaned_data["control_id"]
            analyser = form.cleaned_data["analyser_id"]
            operator = form.cleaned_data["operator"]
            note = form.cleaned_data["note"]
            print(result, date, control, analyser, operator, note)
            test = Test(result=result, test_date=date, control_id=Control.objects.get(pk=control), \
                        analyser_id=Analyser.objects.get(pk=analyser), operator=operator, note=note)
            test.save()
            return HttpResponseRedirect(f'/tests/{control}')
    return render(request, 'Qsee/test_input.html', {"form": form})


from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('404Error/', views.qsee_error, name='qsee_error'),
    path('assays/', views.assays, name='assays'),
    path('controls/<assay_id>/', views.controls, name='controls'),
    path('tests/<control_id>/', views.tests, name='tests'),
    path('test_input/<control_id>/<analyser_id>/', views.test_input, name='test_input'),
    path('settings/', views.settings, name='settings'),
    path('settings/assay/', views.settings_assay, name='settings_assay'),
    path('settings/control/', views.settings_control, name='settings_control'),
    path('settings/analyser/', views.settings_analyser, name='settings_analyser')
]
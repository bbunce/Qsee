from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assays/', views.assays, name='assays'),
    path('controls/<assay_id>/', views.controls, name='controls'),
    path('analysers/', views.analysers, name='analysers'),
    path('tests/<control_id>/', views.tests, name='tests'),
    path('test_input/<control_id>', views.test_input, name='test_input'),
    path('settings/', views.settings, name='settings')
]
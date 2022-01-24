from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assays/<int:id>/', views.assays, name='assays'),
    path('controls/', views.controls, name='controls'),
    path('analysers/', views.analysers, name='analysers'),
    path('tests/<int:control_id>/', views.tests, name='tests')
]
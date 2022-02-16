from django.contrib import admin
from .models import Assay, Control, Analyser, Test

# Register your models here.
admin.site.register(Assay)
admin.site.register(Control)
admin.site.register(Analyser)
admin.site.register(Test)
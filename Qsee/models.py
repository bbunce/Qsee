from django.db import models

# Create your models here.
class Assay(models.Model):
    assay_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.assay_name


class Control(models.Model):
    assay_id = models.ForeignKey(Assay, on_delete=models.CASCADE)
    control_name = models.CharField(max_length=50)
    lot_number = models.CharField(max_length=50)
    date_added = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.assay_id}, {self.control_name}, {self.lot_number}, {self.active}"


class Analyser(models.Model):    
    analyser_name = models.CharField(max_length=50)

    def __str__(self):
        return self.analyser_name


class Test(models.Model):
    result = models.FloatField()
    test_date = models.CharField(max_length=200, blank=True)
    control_id = models.ForeignKey(Control, on_delete=models.CASCADE)
    analyser_id = models.ForeignKey(Analyser, on_delete=models.CASCADE)
    operator = models.CharField(max_length=50)
    note = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.test_date}, {self.control_id}, {self.result}"

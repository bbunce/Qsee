from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Global

con_id = 0

# Create your models here.
class Assay(models.Model):
    assay_name = models.CharField(max_length=50)
    analyser_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.assay_name}, {self.analyser_id}"


class Control(models.Model):
    assay_id = models.ForeignKey(Assay, on_delete=models.CASCADE)
    control_name = models.CharField(max_length=50)
    lot_number = models.CharField(max_length=50)
    # date_added = models.DateField()  
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


class MR_ControlChart():
    """ Generate the Westgard visual chart """
    def fit(self, data, dates):
        self.X = data
        self.Y = dates[-15:]
        self.number_of_sample = len(self.X)
        self.mR = np.zeros(((self.number_of_sample - 1), 1))

        for i in range(len(self.mR)):
            self.mR[i] = abs(self.X[i + 1] - self.X[i])

    def ControlChart(self, d2, D4, D3, onesd, average, cov):
        aload = 'SARS_CoV_2'  # TEMPORARY
        # ucl_X = self.X.mean() + (3 / d2 * np.sqrt(self.number_of_sample)) * self.mR.mean()
        ucl_X = self.X.mean() + onesd*3
        cl2_X = self.X.mean() + onesd*2
        cl1_X = self.X.mean() + onesd
        cl_X = self.X.mean()
        # lcl_X = self.X.mean() - (3 / d2 * np.sqrt(self.number_of_sample)) * self.mR.mean()
        cl3_X = self.X.mean() - onesd
        cl4_X = self.X.mean() - onesd*2
        lcl_X = self.X.mean() - onesd*3

        ucl_mR = D4 * self.mR.mean()
        cl_mR = self.mR.mean()
        lcl_mR = D3 * self.mR.mean()
        # Plot an X chart
        plt.switch_backend('Agg')  # Vital! Stops secondary threads generating redundant GUIs.
        plt.figure(figsize=(20, 10))
        xi = list(range(len(self.Y)))
        plt.xticks(xi, self.Y)
        plt.plot(self.X[-15:], marker="o", color="k", label="QC Values")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.plot([ucl_X] * len(self.X[-15:]), color="r", label="UCL={}".format(ucl_X.round(2)))
        plt.plot([cl2_X] * len(self.X[-15:]), color="y", linestyle="dashed", label="+2 Sigma={}".format(cl2_X.round(2)))
        plt.plot([cl1_X] * len(self.X[-15:]), color="g", linestyle="dashed", label="+1 Sigma={}".format(cl1_X.round(2)))
        plt.plot([cl_X] * len(self.X[-15:]), color="b", label="CL={}".format(cl_X.round(2)))
        plt.plot([cl3_X] * len(self.X[-15:]), color="g", linestyle="dashed", label="-1 Sigma={}".format(cl3_X.round(2)))
        plt.plot([cl4_X] * len(self.X[-15:]), color="y", linestyle="dashed", label="-2 Sigma={}".format(cl4_X.round(2)))
        plt.plot([lcl_X] * len(self.X[-15:]), color="r", label="LCL={}".format(lcl_X.round(2)))
        plt.title(aload + " Quality Control Chart")
        # plt.xticks(np.arange(len(self.X)))
        plt.legend(loc='upper left')
        # Defining the co-efficient of variance and uncertainty measures (both absolute and relative)
        plt.figtext(0.5, 0.01, "Measurement of uncertainty (absolute): " + str(round(onesd*2, 2)) + '\n' +
                    "Measurement of uncertainty (relative): " + str(round((1 - ((average - onesd * 2) / average))
                    * 100, 2)) + "%" + '\n' + "Co-efficient of variance: " + str(round(cov, 2)) + "%",
                    fontsize=10, ha="center", bbox={"facecolor": "grey", "alpha": 0.5, "pad": 5})
        #plt.show() - Disabled - starting a Matplotlib GUI outside of the main thread will cause Assertion errors.
        plt.savefig('Qsee/static/' + aload + '.svg', format='svg', dpi=1200)

        # Plot an mR chart
        plt.figure(figsize=(15, 5))
        plt.plot(self.mR, marker="o", color="k", label="mR ")
        plt.plot([ucl_mR] * len(self.X), color="r", label="UCL={}".format(ucl_mR.round(2)))
        plt.plot([cl_mR] * len(self.X), color="b", label="CL={}".format(cl_mR.round(2)))
        plt.plot([lcl_mR] * len(self.X), color="r", label="LCL={}".format(lcl_mR.round(2)))
        plt.title("QC - mR  Chart")
        plt.xticks(np.arange(len(self.X)))
        plt.legend(loc='upper left')
        # plt.show() - DISABLED FOR NOW, COMPLETE

        # Plot a boxplot
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 2, 1)
        plt.boxplot(x=self.X)
        plt.title("QC - Boxplot X")
        plt.xlabel("X")
        plt.subplot(1, 2, 2)
        plt.boxplot(x=self.mR)
        plt.title("QC - Boxplot mR")
        plt.xlabel("mR ")
        # plt.show() - DISABLED FOR NOW, COMPLETE


def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)


def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev

def cid(value):
    global con_id
    con_id = value
    return

def westgard(value):
    """ Perform a Westgard rule check before allowing result submission """
    values = list(Test.objects.filter(control_id = con_id).order_by('id').values_list('result', flat=True))
    onesd = stdev(values)
    total = 0
    for i in values:
        total += i
    average = total / len(values)

    if value > average+onesd*3:
        raise ValidationError(
            _('A 3SD violation has occurred! ' + str(value) + ' exceeds the upper control limit.'),
            params={'value': value},
        )
        return
# QSee quality control monitor - v1.0a
# App is dependent on local CSV files - code should be adapted to utilise API/db storage
# Switch from global variable use to exchanging data through function arguments?
# main.py merge with flask_app/main.py required.
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import csv
import math
from colorama import init, Fore, Back, Style
from datetime import datetime

plt.style.use('seaborn-colorblind')

# Initializes Colorama
init(autoreset=True)

# Global variables
aload = ''  # Stores the name of the assay CSV file
onesd = 0  # Measure of a single standard deviation in the assay
cov = 0  # Co-efficient of variance calculation
qcval = 0  # QC value entry
average = 0  # Mean value
values = []  # List containing all previous results


# Class for generating a moving range chart
class MR_ControlChart:

    def fit(self, data, dates):
        self.X = data
        self.Y = dates[-15:]
        self.number_of_sample = len(self.X)
        self.mR = np.zeros(((self.number_of_sample - 1), 1))

        for i in range(len(self.mR)):
            self.mR[i] = abs(self.X[i + 1] - self.X[i])

    def ControlChart(self, d2, D4, D3):
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
        plt.figtext(0.5, 0.01, "CV: " + str(round(cov, 2)) + "%. Total QC entries: " + str(len(self.X)), fontsize=10,
                    ha="center", bbox={"facecolor": "grey", "alpha": 0.5, "pad": 5})
        plt.show()

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


# Function to check whether string is in float format
def is_float(n: str) -> bool:
    try:
        float(n)
        return True
    except ValueError:
        return False


def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)


def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev


def main_menu():  # Welcome menu
    print('\n' + Style.BRIGHT + Back.BLACK + Fore.GREEN + "QSee Quality Control monitor v1.0a." + '\n')
    # Check if assay.csv exists - if not, create
    if os.path.isfile('assays.csv') is False:
        print(Style.DIM + Back.BLACK + Fore.RED + "Assay file not found. A new file has been created")
        with open('assays.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['ASSAY', 'ANALYSER', 'CONTROL', 'LOT'])
    print("Please select one of the following options:" + '\n')
    print("1. Load existing assay.")
    print("2. Create a new assay." + '\n')
    men = input("Enter value: ")
    if men == "1":
        assay_menu()  # Load the assay menu
    if men == "2":
        new_assay()  # Load the create menu
    if men.isnumeric() is False or int(men) != 1 and int(men) != 2:
        input(Style.DIM + Back.BLACK + Fore.RED + "Invalid choice. Press enter to return to the main menu")
        main_menu()


def assay_menu():
    assays = pd.read_csv(r'assays.csv')
    if len(assays) < 1:  # Check if assay list CSV has any entries.
        print('\n' + Style.DIM + Back.BLACK + Fore.RED + "Assay list is empty. Please add an assay before use.")
        input('\n' + "Press Enter to return to the main menu.")
        main_menu()
    else:
        print('\n' + Style.BRIGHT + Back.BLACK + Fore.BLUE + "CURRENT ASSAYS" + '\n')
        alist = assays['ASSAY'].tolist()
        print(*alist, sep='\n')  # Formats the list generated into individual lines
        global aload
        aload = input('\n' + "Enter assay to load: ")
        if os.path.isfile(aload + '.csv') is True:
            result_menu()
        if os.path.isfile(aload + '.csv') is False:
            print(Style.DIM + Back.BLACK + Fore.RED + "Assay not found. Please ensure spelling is correct.")
            assay_menu()


def new_assay():
    assayname = input('\n' + "Please enter the name of the assay: ")
    analysername = input("Please enter the name of the analyser: ")
    controlname = input("Please enter the name of the assay control: ")
    lotnumber = input("Please enter the current lot number for the assay control: ")
    # NEED TO WRITE A CHECK FOR DUPLICATE ASSAY NAMES HERE
    db = pd.DataFrame([[assayname, analysername, controlname, lotnumber]],
                      columns=['ASSAY', 'ANALYSER', 'CONTROL', 'LOT'])
    db.to_csv(r'assays.csv', mode='a', header=False, index=False)
    # Create a CSV file for the new assay
    with open(assayname + '.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['RESULT', 'DATE', 'CONTROL', 'ANALYSER', 'LOT', 'OPERATOR', 'NOTE'])
    # Print to inform user in terminal
    print('\n' + Style.BRIGHT + Back.GREEN + Fore.WHITE + "Assay created successfully!")
    input('\n' + "Press enter to return to the main menu")
    main_menu()


def result_menu():
    print('\n' + Style.BRIGHT + Back.BLACK + Fore.GREEN + aload + " QC menu" + '\n')
    current = pd.read_csv(aload + '.csv', on_bad_lines='skip')
    global values
    values = current['RESULT'].tolist()
    values = [float(i) for i in values]  # Converts all values in list to floats
    values2 = np.array(values)
    dates = current['DATE'].tolist()
    dates2 = np.array(dates)
    total = 0
    # Require at least 10 QC entries before any kind of analysis can be made.
    if len(values) < 10:
        print("There are not enough QC entries to formulate an accurate Westgard plot. Currently: " + str(len(values)))
        print("You require at least 10 to begin.")
    else:
        # Takes all QC values in list to generate a global COV and SD figure
        global onesd
        onesd = stdev(values)
        for i in values:
            total += i
        global average
        average = total / len(values)
        global cov
        cov = (onesd / average) * 100
        # Send array of control values to QC chart
        chart = MR_ControlChart()
        chart.fit(values2, dates2)
        chart.ControlChart(d2=1.128, D3=0, D4=3.267)  # Random values for now. Requires assignment for mR chart.
        # Terminal print block
        print("NUMBER OF ENTRIES: " + str(len(values)))
        print("MEAN: " + str(average))
        print("SD+1: " + str(average + onesd))
        print("SD+2: " + str(average + onesd * 2))
        print("SD+3: " + str(average + onesd * 3))
        print("SD-1: " + str(average - onesd))
        print("SD-2: " + str(average - onesd * 2))
        print("SD-3: " + str(average - onesd * 3))
        print("CV: " + str(cov) + "%")
        # Check COV standard
        if cov < 5:
            print('\n' + Style.BRIGHT + Back.GREEN + Fore.WHITE + "Assay performance is excellent.")
        if 5 < cov < 10:
            print('\n' + Style.BRIGHT + Back.YELLOW + Fore.BLACK + "Assay performance is acceptable")
        if cov > 10:
            print(
                '\n' + Style.BRIGHT + Back.RED + Fore.BLACK + "Co-efficient of variance measurement in this assay is high. ")
    print('\n' + Style.DIM + Back.BLACK + Fore.RED + aload + " assay menu")
    print('\n' + '1. Add new QC data')
    print('2. Modify existing data')
    opt = input('\n' + 'Select an option: ')
    if opt == '1':
        add_qc()
    if opt == '2':
        print("modify")


def add_qc():
    # read csv, and split on "," the line
    csv_file = csv.reader(open('assays.csv', "r"), delimiter=",")

    # loop through the csv list
    for row in csv_file:
        if aload == row[0]:
            print('\n' + 'Current control for this assay is: ' + row[2])
            print('Current lot number for this assay is: ' + row[3])
            dec = input('\n' + 'If these details are correct? (y/n): ')
            if dec == 'y' or dec == 'Y':
                qc = input('\n' + 'Enter the QC value recorded: ')
                if qc.isnumeric() is False and is_float(qc) is False:
                    print("Please enter numeric figures only.")
                    add_qc()
                else:
                    global qcval
                    qcval = float(qc)
                    if len(values) > 9:
                        westgard_check()
                    else:
                        add_db()
            else:
                main_menu()


def westgard_check():
    # 13S UCL/LCL VIOLATION
    if qcval > average+onesd*3:
        print('\n' + Style.DIM + Back.BLACK + Fore.RED + "WARNING! QC value exceeds the upper control limit.")
        print('Current upper control limit: ' + str(round(average+onesd*3, 2)) + '. Your result: ' + str(qcval))
        print('Results produced within this run should be rejected.')
        return
    if qcval < average-onesd*3:
        print('\n' + Style.DIM + Back.LIGHTBLACK_EX + Fore.RED + "WARNING! QC value exceeds the lower control limit.")
        print('Current lower control limit: ' + str(round(average-onesd*3, 2)) + '. Your result: ' + str(qcval))
        print('Results produced within this run should be rejected.')
        return
    # R4S VIOLATION
    if values[-1] > average+onesd*2 and qcval < average-onesd*2:
        print('\n' + Style.DIM + Back.BLACK + Fore.YELLOW + "WARNING! R4S violation has occurred.")
        print('Previous QC value (' + str(values[-1]) + ') was 2 standard deviations above the mean.')
        print('The QC value you entered (' + str(qcval) + ') is 2 standard deviations below the mean.')
        print('This rule should only be interpreted within-run, not between-run.')
        g = input('\n' + 'Confirm result? (y/n): ')
        if g == 'y' or g == 'Y':
            add_db()
        else:
            return
    if values[-1] < average-onesd*2 and qcval > average+onesd*2:
        print('\n' + Style.DIM + Back.BLACK + Fore.YELLOW + "WARNING! R4S violation has occurred.")
        print('Previous QC value (' + str(values[-1]) + ') was 2 standard deviations below the mean.')
        print('The QC value you entered (' + str(qcval) + ') is 2 standard deviations above the mean.')
        print('This rule should only be interpreted within-run, not between-run.')
        g = input('\n' + 'Confirm result? (y/n): ')
        if g == 'y' or g == 'Y':
            add_db()
        else:
            return
    # 22S VIOLATION
    if values[-1] > average+onesd*2 and qcval > average+onesd*2:
        print('\n' + Style.DIM + Back.BLACK + Fore.YELLOW + "WARNING! A 22S violation has occurred.")
        print('Previous QC value (' + str(values[-1]) + ') was 2 standard deviations above the mean.')
        print('The QC value you entered (' + str(qcval) + ') is 2 standard deviations above the mean.')
        print('Please check your laboratory policy before proceeding to enter this result into the database.')
        g = input('\n' + 'Confirm result? (y/n): ')
        if g == 'y' or g == 'Y':
            add_db()
        else:
            return
    if values[-1] < average-onesd*2 and qcval < average-onesd*2:
        print('\n' + Style.DIM + Back.BLACK + Fore.YELLOW + "WARNING! A 22S violation has occurred.")
        print('Previous QC value (' + str(values[-1]) + ') was 2 standard deviations below the mean.')
        print('The QC value you entered (' + str(qcval) + ') is 2 standard deviations below the mean.')
        print('Please check your laboratory policy before proceeding to enter this result into the database.')
        g = input('\n' + 'Confirm result? (y/n): ')
        if g == 'y' or g == 'Y':
            add_db()
        else:
            return
    # 41S VIOLATION
    if values[-3] > average+onesd and values[-2] > average+onesd and values[-1] > average+onesd and qcval > average+onesd:
        print('\n' + Style.DIM + Back.BLACK + Fore.YELLOW + "WARNING! A 41S violation has occurred.")
        print('The last 4 QC values all fall at least 1 standard deviation above the mean.')
        print('The QC value you entered:' + str(qcval))
        print('Please check your laboratory policy before proceeding to enter this result into the database.')
        g = input('\n' + 'Confirm result? (y/n): ')
        if g == 'y' or g == 'Y':
            add_db()
        else:
            return
    if values[-3] < average-onesd and values[-2] < average-onesd and values[-1] < average-onesd and qcval < average-onesd:
        print('\n' + Style.DIM + Back.BLACK + Fore.YELLOW + "WARNING! A 41S violation has occurred.")
        print('The last 4 QC values all fall at least 1 standard deviation below the mean.')
        print('The QC value you entered:' + str(qcval))
        print('Please check your laboratory policy before proceeding to enter this result into the database.')
        g = input('\n' + 'Confirm result? (y/n): ')
        if g == 'y' or g == 'Y':
            add_db()
        else:
            return
    add_db()


def add_db():
    # Add result to database
    with open(aload + '.csv', 'a') as csvfile:
        # csvfile.write("\n")  # write new line
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([qcval, datetime.utcnow().today().strftime('%d/%m/%Y'), 'CONTROL', 'ANALYSER', 'LOT', 'OPERATOR', 'NOTE'])
        print('\n' + Style.BRIGHT + Fore.GREEN + 'Result added to database')


# Script workflow - initiate the code
main_menu()
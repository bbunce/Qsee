# Qsee: Quality Control Management System
Developed by George Doyle and Ben Bunce

### Project description

QSee is a quality control visualisation tool that allows users to monitor internal quality control data through the generation of Levey-Jennings plots (matplotlib) and the automatic application of Westgard rules.

![Screenshot of the dashboard](/screen1.png "Screenshot of the dashboard")

Qsee facilitates conformance with ISO 15189:2012 standards and provides a simple mechanism for analysing trends. The following Westgard rules are applied to control results:

![Screenshot of the dashboard](/screen2.png "Westgard table list")

QSee is based on the Django framework and stores records in a pre-populated SQLite relational database that links assays to controls, analysers, lot numbers and individual results.


### Installation
- Clone the github ```<branch>``` repository.
- Set up a new virtual environment of your choice.

### Dependencies
- The list of required packages can be found in the ```requirements.txt``` file. 
- Install the all the packages ```pip install -r requirements.txt```

### Setup
- Activate virtual environment.
- Navigate to the root folder that contains the ```manage.py``` file.
- Start Django server ```python3 manage.py runserver```.
- Navigate to localhost or http://127.0.0.1:8000/ in your browser.

### Instructions
#### Home Page
- 3 navigational buttons; Home, Assays and Settings are navigation buttons that are always visible from any page.

#### Assays
- Lists all available assays the laboratory have added to the Qsee system.

##### Controls
- Clicking on an assay will display all the available controls associated with that assay.
##### Quality Report
- Displays quality control graph for each set of control data for under each different analyser it has been used on.
##### Add control data
- Clicking on this link will take the user to a form in which the test control data can be added to the database.
- If the user wants to start recording testing data on a new analyser, a list of available analysers can be selected at the bottom of the page.
##### Input control data
- Form for the user to input the control testing data
- Click save to save the record.
##### Example usage - viewing and amending quality control records for SARS_CoV_2
- Load the home page
- Click 'Assays'
- Click 'SARS_CoV_2'
- Click 'Control: n_gene_pos | Lot: 237347/A | Active: True'
- Quality control graphs and metrics will be displayed on screen.
- Click 'Add control data'
- Enter a valid control and date. Entries that breach Westgard rulings will not be validated and will flag an error to alert the user
- The graph and quality metrics will automatically update

### Settings
- New assays, control and analysers can be added to the system.

### Contact Us
- [George Doyle](mailto:george.doyle@postgrad.manchester.ac.uk?subject=[QSee])
- Ben Bunce <email>

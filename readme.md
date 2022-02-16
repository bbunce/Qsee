# Qsee: Quality Control Management System
Developed by George Doyle and Ben Bunce

### Project description


### Installation
- Clone the github ```<branch>``` repositry.
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

### Settings
- New assays, control and analysers can be added to the system.

### Contact Us
- George Doyle <email>
- Ben Bunce <email>

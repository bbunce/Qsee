from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# Set environment paths type the following commands into the terminal
# export FLASK_APP=flask_app/main.py
# export FLASK_ENV=development
# Run flask application by typing flask run
# *** DO FIRST ***
# Before running this script for the first time a database needs to be created
# in the database. Open the python console and type the following...
# from main import db
# db.create_all()

# create flask object
app = Flask(__name__)
# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create a database object
db = SQLAlchemy(app)


# define database table and attributes
# example...
class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assay_type = db.Column(db.String(80))
    value = db.Column(db.Float)
    # analyser = db.Column(db.String(80), unique=False, nullable=False)
    # date = db.Column(db.DateTime, unique=False, nullable=False)
    # lot = db.Column(db.String(80), unique=False, nullable=False)
    # current_control = db.Column(db.Boolean, nullable=True)
    # # total_runs = can be a sum of assay_types and/or lot
    # repeated = db.Column(db.Boolean)
    # corrective_action = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"{self.assay_type} - {self.value}"


@app.route('/')
def home():
    return "Qsee homepage"


@app.route('/view/')
def view_values():
    values = Value.query.all()
    output = []
    for value in values:
        value_data = {'assay_type': value.assay_type, 'value': value.value}
        output.append(value_data)
    return {"values": output}


@app.route('/add/', methods=['POST'])
def add_values():
    value = Value(assay_type=request.json['assay_type'], value=request.json['value'])
    db.session.add(value)
    db.session.commit()
    return {'id': value.id}


if __name__ == "__main__":
    app.run()

# Qsee: Quality Control Management System

### Dependencies
```pip install requirements.txt```
### Environment
Set environment paths

```export FLASK_APP=flask_app/main.py```

```export FLASK_ENV=development```

Run flask application

```flask run```

## Database setup
Database creation required before initially running application.

Open python interpreter (i.e. type ```python``` into the terminal)

```
>>> from main import db
>>> from main import Value
>>> db.create_all()
```

### Adding records using python interpreter
```
>>> r = Value(assay_type="covid-19 pos", value=19.0)
>>> db.session.add(r)
>>> db.session.commit()
>>> Value.query.all()
[covid-19 pos - 19.0]
>>> r = Value(assay_type="RNA spike", value=44.0)
>>> db.session.add(r)
>>> db.session.commit()
>>> Value.query.all()
[covid-19 pos - 19.0, RNA spike - 44.0]
```

### Adding records using JSON

Run python ```add_data_db.py```. Comment out to use either manual / file method.

### Delete records using python interpreter
```
>>> Value.query.filter(Value.id == 1).delete()
>>> Value.query.filter(Value.assay_type == "covid-19 pos").delete()
```


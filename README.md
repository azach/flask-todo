# This app is built on Flask and Backbone.

## To start:

* cd into the todo workspace
* Install dependencies with `pip install -r requirements.txt`
* Create your database in a python console with:
```python
from todo import db
db.create_all()
```
* Run `python todo.py` from the command line.
* Navigate to http://127.0.0.1:5000/ in a browser.

## To run tests:

* cd into the todo workspace
* Install dependencies with `pip install -r requirements.txt`
* Run `python todo_tests.py` from the command line.

import os
import json
import sqlite3
from flask import Flask, g, Response

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'todo.db'),
    DEBUG=True,
    SECRET_KEY='12345',
    USERNAME='admin',
    PASSWORD='default'
))

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row))

def query_db(query, args=()):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Routing

@app.route("/")
def hello():
  return 'hello world!'

@app.route("/tasks")
def index():
    results = query_db('select id, text, completed from tasks')
    return Response(json.dumps(results), mimetype='application/json')

@app.route("/tasks", methods=['POST'])
def create():
    return "Created a task!"

if __name__ == "__main__":
    app.run()

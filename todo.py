import json
import os
import sqlite3
from flask import Flask, g, jsonify, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import between

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/todo.db'
db = SQLAlchemy(app)

# Models

class Task(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    text      = db.Column(db.String(120), unique=False)
    completed = db.Column(db.Boolean, unique=False)
    position  = db.Column(db.Integer, unique=False)

    def __init__(self, text, completed, position):
        self.text      = text
        self.completed = completed
        self.position  = position

    def __repr__(self):
        return '<Task %r>' % str(self.position)

    @property
    def to_json(self):
        return {
            'id'        : self.id,
            'text'      : self.text,
            'completed' : self.completed,
            'position'  : self.position
        }

# Routing

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/tasks")
def index():
    results = Task.query.order_by(Task.position.asc()).all()
    return json.dumps([i.to_json for i in results])

@app.route("/tasks", methods=['POST'])
def create():
    next_position = (db.session.query(func.max(Task.position)).scalar() or -1) + 1
    task = Task(request.json["text"], False, next_position)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_json)

@app.route("/tasks/<task_id>", methods=['PUT'])
def update(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if request.json.has_key('position'):
        old_position = task.position
        new_position = request.json['position']

        if old_position < new_position:
            reordered_tasks = Task.query.filter(Task.position.between(old_position + 1, new_position)).all()

            for reordered_task in reordered_tasks:
                reordered_task.position = reordered_task.position - 1
        else:
            reordered_tasks = Task.query.filter(Task.position.between(new_position, old_position - 1)).all()

            for reordered_task in reordered_tasks:
                reordered_task.position = reordered_task.position + 1

        task.position = new_position

    if request.json.has_key('completed'):
        task.completed = request.json['completed']
    db.session.commit()
    return jsonify(task.to_json)

if __name__ == "__main__":
    app.run(debug=True)

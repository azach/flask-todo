import os
import sqlite3
from flask import Flask, g, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/todo.db'
db = SQLAlchemy(app)

# Models

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), unique=False)
    completed = db.Column(db.Boolean, unique=False)

    def __init__(self, text, completed):
        self.text = text
        self.completed = completed

    def __repr__(self):
        return '<Task %r>' % self.text

    @property
    def to_json(self):
        return {
            'id'        : self.id,
            'text'      : self.text,
            'completed' : self.completed
        }

# Routing

@app.route("/")
def hello():
    return 'hello world!'

@app.route("/tasks")
def index():
    results = Task.query.all()
    return jsonify(tasks=[i.to_json for i in results])

@app.route("/tasks", methods=['POST'])
def create():
    task = Task(request.form['text'], 0)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_json)

@app.route("/tasks/<task_id>", methods=['PUT'])
def update(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.completed = 1 if request.form['completed'] == '1' else 0
    db.session.commit()
    return jsonify(task.to_json)

if __name__ == "__main__":
    app.run(debug=True)

import json
import todo
import unittest

from todo import db, Task

class TodoTestCase(unittest.TestCase):

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/todo_test.db'

    def setUp(self):
        todo.app.config['TESTING'] = True
        self.app = todo.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_responds_successfully(self):
      assert '200 OK' == self.app.get('/').status

    def test_tasks_index_with_no_tasks(self):
        rv = self.app.get('/tasks')
        assert [] == json.loads(rv.data)

    def test_tasks_index_with_tasks(self):
        task_1 = Task('some task', 0)
        task_2 = Task('some other task', 1)
        db.session.add(task_1)
        db.session.add(task_2)
        db.session.commit()

        rv = self.app.get('/tasks')
        assert [task_1.to_json, task_2.to_json] == json.loads(rv.data)

    def test_tasks_create_invalid_task(self):
        rv = self.app.post('/tasks')
        assert '400 BAD REQUEST' == rv.status

    def test_tasks_create_valid_task(self):
        rv = self.app.post('/tasks', data=dict(text='a new task!'))
        assert {"completed": False, "id": 1, "text": "a new task!"} == json.loads(rv.data)

    def test_tasks_completing_existing_task(self):
        task = Task('some task', 0)
        db.session.add(task)
        db.session.commit()

        rv = self.app.put('/tasks/' + str(task.id), data=dict(completed='1'))
        assert {"completed": True, "id": 1, "text": "some task"} == json.loads(rv.data)

    def test_tasks_uncompleting_existing_task(self):
        task = Task('some task', 1)
        db.session.add(task)
        db.session.commit()

        rv = self.app.put('/tasks/' + str(task.id), data=dict(completed='0'))
        assert {"completed": False, "id": 1, "text": "some task"} == json.loads(rv.data)

if __name__ == '__main__':
    unittest.main()

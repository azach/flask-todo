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
      assert '200 OK' in self.app.get('/').status

    def test_tasks_index_with_no_tasks(self):
        rv = self.app.get('/tasks')
        assert {"tasks": []} == json.loads(rv.data)

    def test_tasks_index_with_tasks(self):
        task_1 = Task('some task', 0)
        task_2 = Task('some other task', 1)
        db.session.add(task_1)
        db.session.add(task_2)
        db.session.commit()

        rv = self.app.get('/tasks')
        assert {"tasks": [task_1.to_json, task_2.to_json]} == json.loads(rv.data)

if __name__ == '__main__':
    unittest.main()

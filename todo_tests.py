import json
import todo
import unittest

from todo import db, Task

class TodoTestCase(unittest.TestCase):

    def setUp(self):
        todo.app.config['TESTING'] = True
        todo.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/todo_test.db'
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
        task_1 = Task('some task', False)
        task_2 = Task('some other task', True)
        db.session.add(task_1)
        db.session.add(task_2)
        db.session.commit()

        rv = self.app.get('/tasks')
        assert [task_1.to_json, task_2.to_json] == json.loads(rv.data)

    def test_tasks_index_with_ordered_tasks(self):
        task_3 = Task('some task', False, 2)
        task_2 = Task('some other task', True, 1)
        task_1 = Task('some other task', True, 0)
        db.session.add(task_3)
        db.session.add(task_2)
        db.session.add(task_1)
        db.session.commit()

        rv = self.app.get('/tasks')
        assert [task_1.to_json, task_2.to_json, task_3.to_json] == json.loads(rv.data)

    def test_tasks_create_invalid_task(self):
        rv = self.app.post('/tasks', data={}, content_type='application/json')
        assert '400 BAD REQUEST' == rv.status

    def test_tasks_create_valid_task(self):
        rv = self.app.post('/tasks', content_type='application/json', content_length=21, data=json.dumps({'text': 'a new task!'}))
        assert {"completed": False, "id": 1, "text": "a new task!", "position": 0} == json.loads(rv.data)

    def test_tasks_completing_existing_task(self):
        task = Task('some task', False)
        db.session.add(task)
        db.session.commit()

        rv = self.app.put('/tasks/' + str(task.id), content_type='application/json', content_length=16, data=json.dumps({'completed': True}))
        assert {"completed": True, "id": 1, "text": "some task", "position": 0} == json.loads(rv.data)

    def test_tasks_uncompleting_existing_task(self):
        task = Task('some task', True)
        db.session.add(task)
        db.session.commit()

        rv = self.app.put('/tasks/' + str(task.id), content_type='application/json', content_length=16, data=json.dumps({'completed': False}))
        assert {"completed": False, "id": 1, "text": "some task", "position": 0} == json.loads(rv.data)

    def test_tasks_reordering_existing_task_response(self):
        task_1 = Task('task 1', False, 0)
        task_2 = Task('task 2', False, 1)
        db.session.add(task_1)
        db.session.add(task_2)
        db.session.commit()

        rv = self.app.put('/tasks/' + str(task_1.id), content_type='application/json', content_length=11, data=json.dumps({'position': 1}))
        assert {"completed": False, "id": 1, "text": "task 1", "position": 1} == json.loads(rv.data)

    def test_tasks_reordering_existing_task(self):
        task_1 = Task('task 1', False, 0)
        task_2 = Task('task 2', False, 1)
        task_3 = Task('task 3', False, 2)
        task_4 = Task('task 4', False, 3)
        db.session.add(task_1)
        db.session.add(task_2)
        db.session.add(task_3)
        db.session.add(task_4)
        db.session.commit()

        rv = self.app.put('/tasks/' + str(task_3.id), content_type='application/json', content_length=11, data=json.dumps({'position': 1}))
        assert [0, 2, 1, 3] == map(lambda task: task.position, Task.query.order_by(Task.id.asc()).all())

if __name__ == '__main__':
    unittest.main()

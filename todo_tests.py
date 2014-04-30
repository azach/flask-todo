import os
import todo
import unittest
import tempfile

class TodoTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, todo.app.config['DATABASE'] = tempfile.mkstemp()
        todo.app.config['TESTING'] = True
        self.app = todo.app.test_client()
        todo.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(todo.app.config['DATABASE'])

    def test_index_responds_successfully(self):
      assert '200 OK' in self.app.get('/').status

    def test_tasks_index_with_no_tasks(self):
        rv = self.app.get('/tasks')
        assert '' in rv.data

if __name__ == '__main__':
    unittest.main()

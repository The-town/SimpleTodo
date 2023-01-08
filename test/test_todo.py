import datetime
import os
import unittest


from todo import Todo


class TestTodo(unittest.TestCase):
    def setUp(self) -> None:
        self.format: str = "[todo][B][#%Y-%m-%d]test_delta.txt"
        expired_todo_name: str = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=1),
                                                            self.format)
        no_expired_todo_name: str = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1),
                                                               self.format)
        self.todo_names: list = [expired_todo_name, no_expired_todo_name]
        self.todos: list = []
        for name in self.todo_names:
            with open(name, "w") as f:
                f.close()
            self.todos.append(Todo(name))

    def test_get_delta_today_and_limit_date(self) -> None:
        now_year: int = datetime.datetime.now().year
        now_month: int = datetime.datetime.now().month
        now_day: int = datetime.datetime.now().day
        now: datetime.datetime = datetime.datetime(now_year, now_month, now_day)

        for todo in self.todos:
            todo_delta: str = todo.get_delta_today_and_limit_date()
            delta: datetime.timedelta = \
                datetime.datetime.strptime(os.path.basename(todo.path), self.format) - now

            self.assertEqual(todo_delta, str(delta.days))

    def tearDown(self) -> None:
        for todo_name in self.todo_names:
            os.remove(todo_name)

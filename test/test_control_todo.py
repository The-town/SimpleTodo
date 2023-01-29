import datetime
import os
import unittest
from typing import List

from todo import ControlTodo, Todo


class TestControlTodo(unittest.TestCase):
    def setUp(self) -> None:
        self.control_todo: ControlTodo = ControlTodo()
        self.todo: Todo = Todo("F:\\Document\\800_IT自己学習\\09_python\\21_todo\\test\\[todo][B][#][#test]test_todo.txt")

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

    def test_get_content_todo_for_display_list(self):
        content_for_display: str = self.control_todo.get_content_todo_for_display_list(self.todo)
        self.assertEqual(content_for_display, "test_todo  カテゴリ:#test")

    def test_search_file_until_spec_date(self) -> None:
        todos_day_0: List[Todo, ...] = self.control_todo.search_file_until_spec_date(0)
        self.assertEqual(todos_day_0, [self.todos[0], ])

        todos_day_1: List[Todo, ...] = self.control_todo.search_file_until_spec_date(1)
        self.assertEqual(todos_day_1, [self.todos[0], ])

        todos_day_2: List[Todo, ...] = self.control_todo.search_file_until_spec_date(2)
        self.assertEqual(todos_day_2, self.todos)

    def tearDown(self) -> None:
        for todo_name in self.todo_names:
            os.remove(todo_name)


if __name__ == '__main__':
    unittest.main()

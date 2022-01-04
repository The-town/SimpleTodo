import unittest
from todo import ControlTodo, Todo


class TestControlTodo(unittest.TestCase):
    def setUp(self) -> None:
        self.control_todo: ControlTodo = ControlTodo()
        self.todo: Todo = Todo("F:\\Document\\800_IT自己学習\\09_python\\21_todo\\test\\[todo][B][#][#test]test_todo.txt")

    def test_get_content_todo_for_display_list(self):
        content_for_display: str = self.control_todo.get_content_todo_for_display_list(self.todo)
        self.assertEqual(content_for_display, "test_todo カテゴリ:#test")


if __name__ == '__main__':
    unittest.main()

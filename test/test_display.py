import unittest
from todo import Todo
from display import TodoDetailDisplay


class TestTodoDetailDisplay(unittest.TestCase):
    def setUp(self) -> None:
        self.todo: Todo = Todo("F:\\Document\\800_IT自己学習\\09_python\\21_todo\\test\\[todo][B][#][#test]test_todo.txt")
        self.detail = TodoDetailDisplay(todo=self.todo)

    def test_get_lines_url(self):
        self.todo.detail = "test\nhttps://hogehoge\ntesthttp://hogehoge\nhttp://hogehoge"
        self.assertEqual(self.detail.get_lines_url(), (1, 3))

    def test_get_lines_url_no_url(self):
        self.todo.detail = "test\ntest\ntest"
        self.assertEqual(self.detail.get_lines_url(), ())



if __name__ == '__main__':
    unittest.main()

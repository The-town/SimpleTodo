import unittest
from validate import validate_todo_name


class TestValidate(unittest.TestCase):
    def test_validate_todo_name_in_backslash(self):
        todo_name: str = "\\test1_(@)#"
        is_validate, error_msg = validate_todo_name(todo_name)

        self.assertFalse(is_validate)
        self.assertEqual(error_msg, "\\は名前に使えません。")

    def test_validate_todo_name_in_slash(self):
        todo_name: str = "tes/t1_(@)#"
        is_validate, error_msg = validate_todo_name(todo_name)

        self.assertFalse(is_validate)
        self.assertEqual(error_msg, "/は名前に使えません。")

    def test_validate_todo_name_in_dot(self):
        todo_name: str = "tes.t1_(@)#"
        is_validate, error_msg = validate_todo_name(todo_name)

        self.assertFalse(is_validate)
        self.assertEqual(error_msg, ".は名前に使えません。")


if __name__ == '__main__':
    unittest.main()

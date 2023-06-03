import os
import unittest
from validate import validate_todo_name_empty, validate_todo_name, validate_double_todo_name, validate_todo_limit


class TestValidate(unittest.TestCase):
    def test_validate_todo_name_is_empty(self):
        todo_name: str = ""
        is_validate, error_msg = validate_todo_name_empty(todo_name)

        self.assertFalse(is_validate)
        self.assertEqual(error_msg, "名前を入力してください")

    def test_validate_todo_name_is_not_empty(self):
        todo_name: str = " a"
        is_validate, error_msg = validate_todo_name_empty(todo_name)

        self.assertTrue(is_validate)
        self.assertEqual(error_msg, "")

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

    def test_validate_todo_name_in_full_width_space(self):
        todo_name: str = "tes　t1_(@)#"
        is_validate, error_msg = validate_todo_name(todo_name)

        self.assertFalse(is_validate)
        self.assertEqual(error_msg, "全角スペースは名前に使えません。")

    def test_validate_todo_name_in_half_width_space(self):
        todo_name: str = "tes t1_(@)#"
        is_validate, error_msg = validate_todo_name(todo_name)

        self.assertFalse(is_validate)
        self.assertEqual(error_msg, "半角スペースは名前に使えません。")

    def test_validate_double_todo_name_True(self):
        is_validate, error_msg = validate_double_todo_name("test_tod", os.getcwd())

        self.assertTrue(is_validate)
        self.assertEqual(error_msg, "")

    def test_validate_double_todo_name_False(self):
        is_validate, error_msg = validate_double_todo_name("[todo][B][#][#test]test_todo.txt", os.getcwd())

        self.assertFalse(is_validate)
        self.assertEqual(error_msg, "[todo][B][#][#test]test_todo.txtは既存のTODO名と重複しています。")

    def test_validate_todo_limit_True(self):
        is_validate, error_msg = validate_todo_limit("2023-01-01")

        self.assertTrue(is_validate)
        self.assertEqual(error_msg, "")

    def test_validate_todo_limit_False(self):
        is_validate, error_msg = validate_todo_limit("2023-01-")
        self.assertFalse(is_validate)

        is_validate, error_msg = validate_todo_limit("2023-01-100")
        self.assertFalse(is_validate)

        is_validate, error_msg = validate_todo_limit("2023-13-10")
        self.assertFalse(is_validate)

        is_validate, error_msg = validate_todo_limit("2023-13-a")
        self.assertFalse(is_validate)


if __name__ == '__main__':
    unittest.main()

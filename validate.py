from typing import Tuple
import os


def validate_todo_name_empty(todo_name: str) -> Tuple[bool, str]:
    """
    TODOファイルの名前が空文字列かチェックする関数

    Parameters
    ----------
    todo_name: str
        todoファイルの名前

    Returns
    -------
    Bool: bool, error_msg: str
        バリデーションチェックに成功したかどうか、および失敗時のエラーメッセージ
    """
    if todo_name == "":
        return False, "名前を入力してください"
    return True, ""


def validate_todo_name(todo_name: str) -> Tuple[bool, str]:
    """
    TODOファイルの名前をチェックする関数

    Parameters
    ----------
    todo_name: str
        todoファイルの名前

    Returns
    -------
    Bool: bool, error_msg: str
        バリデーションチェックに成功したかどうか、および失敗時のエラーメッセージ
    """
    not_use_strings: list = ["/", ".", "\\"]

    for not_use_string in not_use_strings:
        if not_use_string in set(todo_name):
            return False, f"{not_use_string}は名前に使えません。"
    return True, ""


def validate_double_todo_name(todo_name: str, todo_path: str) -> Tuple[bool, str]:
    """
    TODOファイルの名前が重複していないかチェックする関数

    Parameters
    ----------
    todo_name: str
        todoファイルの名前
    todo_path: str
        todoファイルのパス

    Returns
    -------
    Bool: bool, error_msg: str
        バリデーションチェックに成功したかどうか、および失敗時のエラーメッセージ
    """

    if os.path.lexists(os.path.join(todo_path, todo_name)):
        return False, f"{todo_name}は既存のTODO名と重複しています。"
    return True, ""

import datetime
from typing import Tuple
import os


def validate_update_todo(todo_path: str, todo_name: str, todo_file_name: str) -> Tuple[bool, str]:
    """
    TODOファイルの名前を更新する際に実行するチェック関数

    Parameters
    ----------
    todo_path: str
    todo_name: str
    todo_file_name: str

    Returns
    -------
     is_validate, error_msg: Tuple[bool, str]
    """
    is_validate_name_empty, error_msg_empty = validate_todo_name_empty(todo_name)
    is_validate_name, error_msg_name = validate_todo_name(todo_name)
    is_validate_double_name, error_msg_double_name = validate_double_todo_name(todo_file_name, todo_path)

    is_validate: bool = is_validate_name_empty and is_validate_name and is_validate_double_name

    error_msg: str = ""
    if not is_validate:
        error_msg = "\n".join([error_msg_empty, error_msg_name, error_msg_double_name])

    return is_validate, error_msg


def validate_add_todo(todo_path: str, todo_name: str, todo_file_name: str, todo_limit: str) -> Tuple[bool, str]:
    is_validate_name_empty, error_msg_empty = validate_todo_name_empty(todo_name)
    is_validate_name, error_msg_name = validate_todo_name(todo_name)
    is_validate_double_name, error_msg_double_name = validate_double_todo_name(todo_file_name, todo_path)
    is_validate_limit, error_msg_limit = validate_todo_limit(todo_limit)

    is_validate: bool = is_validate_name_empty and is_validate_name and is_validate_double_name and is_validate_limit
    error_msg: str = "\n".join([error_msg_empty, error_msg_name, error_msg_double_name, error_msg_limit])

    if is_validate:
        return True, ""
    else:
        return False, error_msg


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
    not_use_strings: list = ["/", ".", "\\", "　", " "]

    for not_use_string in not_use_strings:
        if not_use_string in set(todo_name):
            if not_use_string == "　":
                return False, f"全角スペースは名前に使えません。"
            if not_use_string == " ":
                return False, "半角スペースは名前に使えません。"
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

def validate_todo_limit(todo_limit: str) -> Tuple[bool, str]:
    """
    TODOファイルの期限が正しい形式になっているかチェックする関数

    Parameters
    ----------
    todo_limit : str

    Returns
    -------
    Tuple[bool, str]
    """
    try:
        datetime.datetime.strptime(todo_limit, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "期限のフォーマットが間違っています。\nYYYY-MM-DDとしてください。"

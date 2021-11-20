from typing import Tuple


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


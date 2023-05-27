from typing import Tuple, List


from operate_file_1 import get_all_files
import config
from mail import Imap
import re
import os
import datetime
import uuid
import hashlib


class Todo:
    """
    Todoの各属性値を保持する

    Attributes
    -----------
    name: str
        todo名
    path: str
        todoファイルのパス
    """
    def __init__(self, path: str) -> None:
        self.name: str = ""
        self.detail: str = ""
        self.path: str = path
        self.importance: str = "default"
        self.importance_color: str = "white"
        self.create_time: str = ""
        self.update_time: str = ""
        self.metadata: dict = {}

        self.set_name_from_path()
        self.set_importance_from_filename()
        self.set_metadata_from_filename()
        self.set_todo_timestamp()
        self.get_todo_detail()

        self.delta: str = self.get_delta_today_and_limit_date()

    def __eq__(self, other):
        return self.name == other.name

    def set_name_from_path(self) -> None:
        """
        パスからtodo名を抽出して設定するメソッド

        Returns
        -------
        None
        """
        # [t0d0]xxxx.txt -> [t0d0]xxxx
        self.name = os.path.basename(self.path).split(".")[0]

        # [t0d0]xxxx -> xxxx
        self.name = self.name.split(config.rule_file["string_when_add_todo"]["head"])[1]

    def set_importance_from_filename(self) -> None:
        """
        ファイル名から重要度を設定するメソッド

        Returns
        -------
        None
        """
        pattern = r"\[[{0}]\]".format(
            "|".join(
                [key.upper() for key in config.rule_file["Importance_color"].keys()]
            )
        )
        re_pattern = re.compile(pattern)
        if re_pattern.search(self.name):
            self.importance = re_pattern.search(self.name).group()[1]
        else:
            self.importance = "default"
        self.importance_color = config.rule_file["Importance_color"][self.importance]

    def set_metadata_from_filename(self) -> None:
        """
        ファイル名からメタデータを設定する関数

        Returns
        -------
        None
        """
        # "[A][#meta1][#meta2]test.txt" -> ["#meta1", "#meta2"]
        metadata_list: list = [metadata for metadata in re.split(r"[\[\]]", self.name)[:-1] if "#" in metadata]

        if metadata_list:
            for i, metadata in enumerate(metadata_list):
                if metadata != "#":
                    self.metadata[list(config.rule_file["Meta_data"].keys())[i]] = metadata

    def set_todo_timestamp(self) -> None:
        """
        TODOファイルが作成・更新されたタイムスタンプを設定するメソッド

        Returns
        -------
        create_time, update_time: Tuple[str, str]
            作成日時と更新日時
        """
        stat_result = os.stat(self.path)
        self.create_time = datetime.datetime.fromtimestamp(stat_result.st_ctime).strftime("%Y/%m/%d %H:%M:%S")
        self.update_time = datetime.datetime.fromtimestamp(stat_result.st_mtime).strftime("%Y/%m/%d %H:%M:%S")

    def get_todo_detail(self) -> None:
        """
        TODOファイルの詳細情報を取得するメソッド

        Returns
        --------
        None
        """
        try:
            with open(self.path, encoding="utf_8") as f:
                self.detail = f.read()
        except UnicodeDecodeError:
            self.detail = "このファイルはプレビューできません。"

    def get_delta_today_and_limit_date(self) -> str:
        """
        期限日と今日の差を設定するメソッド

        Returns
        --------
        str(delta.days): str
            期限日と今日の差分
        """
        if "limit" not in self.metadata.keys():
            return ""

        limit_date: datetime.datetime = datetime.datetime.strptime(self.metadata["limit"][1:], "%Y-%m-%d")

        now_year: int = datetime.datetime.now().year
        now_month: int = datetime.datetime.now().month
        now_day: int = datetime.datetime.now().day
        delta: datetime.timedelta = limit_date - datetime.datetime(now_year, now_month, now_day)

        return str(delta.days)


class TodoFromMail:
    """
    メールから追加されたTODOを表すクラス
    """
    def __init__(self):
        self.imap = Imap()
        self.content_of_messages = ()

    def set_content_of_messages(self):
        self.imap.login()
        self.content_of_messages = self.imap.get_content_of_messages()

    def create_todo_files(self) -> None:
        """
        TODOファイルを作成するメソッド

        Returns
        -------
        None
        """
        hash_list = []
        if os.path.isfile("./mail_hash_list.log"):
            with open("./mail_hash_list.log", "r", encoding="utf-8") as f:
                hash_list = f.read().split("\n")

        contents: tuple = self.create_todo_contents()
        for content in contents:
            if self.create_hash_from_mail_body(content["body"]) in hash_list:
                continue

            file_path = os.path.join(config.rule_file["AddTodoFromMail"]["dir_path"], content["title"])
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content["body"])

            self.update_add_hash_list(content["body"])

    def create_todo_contents(self) -> tuple:
        """
        TODOファイルの中身を作成するメソッド

        Returns
        -------
        contents: tuple
        """
        contents = []
        for content_of_message in self.content_of_messages:
            content = {
                "title": f"[todo][C]{content_of_message['subject']}_{str(uuid.uuid4())}.txt",
                "body": f"{content_of_message['body']}"
            }
            contents.append(content)

        return tuple(contents)

    @staticmethod
    def create_hash_from_mail_body(body: str) -> str:
        """
        メールを識別するためにbodyからハッシュ値を生成するメソッド
        Parameters
        ----------
        body : str

        Returns
        -------
        sha256.hexdigest(): str
        """
        sha256 = hashlib.sha256()
        sha256.update(body.encode())
        return sha256.hexdigest()

    def update_add_hash_list(self, body: str):
        """
        同じメールを登録しないように、メールのbodyから取得したハッシュ値を記録するメソッド

        Parameters
        ----------
        body : str

        Returns
        -------
        None
        """
        with open("./mail_hash_list.log", "a", encoding="utf-8") as f:
            f.write(self.create_hash_from_mail_body(body))
            f.write("\n")

class ControlTodo:
    """
    TODOを管理するためのクラス

    Attributes
    -----------
    dir_names_items: dict
    dir_name_keys: list
        TODOファイルがないか探索するディレクトリ名
    dir_paths: list
        TODOファイルがないか探索するディレクトリのパス名
    patterns: list
        TODOファイルの名前パターン
    """

    def __init__(self):

        self.dir_names_items: dict = dict(config.rule_file["Dir_names"].items())
        self.dir_name_keys = list(config.rule_file["Dir_names"].keys())
        self.dir_paths = [config.rule_file["Dir_names"][key] for key in config.rule_file["Dir_names"].keys()]
        self.patterns = [config.rule_file["File_names"][key] for key in config.rule_file["File_names"].keys()]

    def get_paths_which_result_of_search(self, directory_name):
        if directory_name == "all" or directory_name == "":
            return self.search_file()
        else:
            return self.limit_search_file(directory_name)

    def search_file(self):
        """
        全てのTODOファイルを取得する関数

        Returns
        -------
        todos: List[Todo]
            Todoオブジェクトのリスト
        """
        todos: List[Todo] = []
        for dir_path in self.dir_paths:
            todos.extend([Todo(path) for path in get_all_files(dir_path, ";".join(self.patterns))])
        return todos

    def limit_search_file(self, dir_name_key):
        """
        指定されたディレクトリ内にあるTODOファイルを取得する関数

        Parameters
        ----------
        dir_name_key: str
            ディレクトリの名前と対になるキー名

        Returns
        --------
        todos: List[Todo]
            Todoオブジェクトのリスト
        """
        todos: List[Todo] = [Todo(path) for path in
                             get_all_files(config.rule_file["Dir_names"][dir_name_key], ";".join(self.patterns))]
        return todos

    def search_file_until_spec_date(self, days: int) -> List:
        """
        指定された日までのTODOファイルを取得する関数

        Parameters
        -----------
        days: int

        Returns
        --------
        todos: List[Todo]
            Todoオブジェクトのリスト
        """
        todos_set_due_date: List[Todo, ...] = [todo for todo in self.search_file() if todo.delta != ""]
        todos: List[Todo, ...] = [todo for todo in todos_set_due_date if int(todo.delta) < days]
        return todos

    def sort_todo(self, todos: List[Todo], method: str):
        if method == "":
            return todos
        elif method == "重要度":
            return self.sort_importance(todos)
        elif method == "期限":
            return self.sort_todo_limit(todos)

    @staticmethod
    def sort_importance(todos: List[Todo]):
        sorted_todos = sorted(todos, key=lambda todo: todo.importance)
        return sorted_todos

    @staticmethod
    def sort_todo_limit(todos: List[Todo]):
        """
        期限順にTODOを並べ変えるメソッド

        Parameters
        -----------
        todos: List[Todo]
            todoオブジェクトのリスト

        Returns
        --------
        並べ替えた後のtodoオブジェクトのリスト
        """
        limited_todos: List[Todo] = [todo for todo in todos if "limit" in todo.metadata.keys()]
        no_limited_todos: List[Todo] = [todo for todo in todos if "limit" not in todo.metadata.keys()]

        sorted_todos: List[Todo] = sorted(limited_todos, key=lambda x: x.metadata["limit"])
        sorted_todos.extend(no_limited_todos)
        return sorted_todos

    def get_dir_name_keys(self):
        return self.dir_name_keys

    @staticmethod
    def close_todo(todo: Todo) -> None:
        """
        TODOファイルをクローズするメソッド
        Parameters
        ----------
        todo: Todo
            クローズするTodoオブジェクト

        Returns
        -------
        None
        """
        todo_path: str = todo.path
        os.rename(todo_path,
                  os.path.join(
                      os.path.dirname(todo_path), os.path.basename(todo_path).replace("todo", "完了"))
                  )

    @staticmethod
    def get_content_todo_for_display_list(todo: Todo) -> str:
        """
        todoをリスト表示する際に使用する文字列を取得するメソッド

        Parameters
        -----------
        todo: Todo
            todoオブジェクト

        Returns
        -------
        " ".join([todo.name, metadata]): str
            表示する文字列
        """
        if todo.delta == "":
            return re.sub(r"\[.*]", "", todo.name)

        limit_info: str = "期限まで"+todo.delta+"日"
        return " ".join([limit_info, re.sub(r"\[.*]", "", todo.name)])

    @staticmethod
    def save_todo(todo: Todo):
        """
        todoを保存するメソッド

        Parameters
        ----------
        todo: Todo
            todoオブジェクト

        Returns
        --------
        None
        """
        with open(todo.path, "w", encoding="utf_8") as todo_file:
            todo_file.write(todo.detail)

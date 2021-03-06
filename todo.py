from typing import Tuple, List

from operate_file_1 import get_all_files
import config
import re
import os
import datetime


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


class ControlTodo:
    def __init__(self):

        self.dir_names_items: dict = dict(config.rule_file["Dir_names"].items())
        self.dir_name_keys = list(config.rule_file["Dir_names"].keys())
        self.dir_names = [config.rule_file["Dir_names"][key] for key in config.rule_file["Dir_names"].keys()]
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
        for dir_name in self.dir_names:
            todos.extend([Todo(path) for path in get_all_files(dir_name, ";".join(self.patterns))])
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
        metadata: str = ""
        for key in todo.metadata.keys():
            metadata = " ".join([metadata, ":".join([config.rule_file["Meta_data"][key], todo.metadata[key]])])

        return " ".join([re.sub(r"\[.*]", "", todo.name), metadata])

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

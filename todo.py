from typing import Tuple, List

from operate_file_1 import get_all_files
import configparser
import re
import os
import datetime
from flatten import flatten


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
        self.path: str = path
        self.importance: str = "Z"

        self.rule_file = configparser.ConfigParser()
        self.rule_file.read("./config.ini", "UTF-8")

    def set_name_from_path(self) -> None:
        """
        パスからファイル名を抽出して設定するメソッド

        Returns
        -------
        None
        """
        self.name = os.path.basename(self.path)

    def set_importance_from_filename(self) -> None:
        """
        ファイル名から重要度を設定するメソッド

        Returns
        -------
        None
        """
        pattern = r"\[[{0}]\]".format(
            "|".join(
                [key.upper() for key in self.rule_file["Importance_color"].keys()]
            )
        )
        re_pattern = re.compile(pattern)
        self.importance = re_pattern.search(self.name)


class ControlTodo:
    def __init__(self):

        self.rule_file = configparser.ConfigParser()
        self.rule_file.read("./config.ini", "UTF-8")

        self.dir_names_items: dict = dict(self.rule_file["Dir_names"].items())
        self.dir_name_keys = list(self.rule_file["Dir_names"].keys())
        self.dir_names = [self.rule_file["Dir_names"][key] for key in self.rule_file["Dir_names"].keys()]
        self.patterns = [self.rule_file["File_names"][key] for key in self.rule_file["File_names"].keys()]

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
            todos = [Todo(path) for path in get_all_files(dir_name, ";".join(self.patterns))]
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
                             get_all_files(self.rule_file["Dir_names"][dir_name_key], ";".join(self.patterns))]
        return todos

    def search_meta_data(self, path) -> list:
        """
        ファイル名に記載されているメタデータを取り出す関数

        Parameters
        ----------
        path: str
            todoファイルのパス

        Returns
        -------
        display_metadata_list: list
            メタデータ
        """
        file_name: str = os.path.basename(path)

        # "[A][#meta1][#meta2]test.txt" -> ["#meta1", "#meta2"]
        metadata_list: list = [metadata for metadata in re.split(r"[\[\]]", file_name)[:-1] if "#" in metadata]

        if metadata_list:
            display_metadata_list = []
            for i, metadata in enumerate(metadata_list):
                if metadata != "#":
                    display_metadata_list.append(":".join([self.rule_file["Meta_data"][str(i+1)], metadata]))
            return display_metadata_list
        else:
            return [""]

    def sort_todo(self, paths, method):
        if method == "":
            return paths
        elif method == "重要度":
            return self.sort_importance(paths)
        elif method == "期限":
            return self.sort_todo_limit(paths)

    @staticmethod
    def sort_importance(self, todos: List[Todo]):
        sorted_todos = sorted(todos, key=lambda todo: todo.importance)
        return sorted_todos

    def sort_todo_limit(self, paths):
        path_dicts = []
        for path in paths:
            path_dict = {}
            first_metadata = self.search_meta_data(path)[0]
            if self.rule_file["Meta_data"]["1"] in first_metadata:
                path_dict["metadata_todo_limit"] = first_metadata.split(":")[-1]
            else:
                path_dict["metadata_todo_limit"] = "9999/12/31"
            path_dict["path"] = path
            path_dicts.append(path_dict)

        sorted_path_dicts = sorted(path_dicts, key=lambda x: x["metadata_todo_limit"])
        sorted_paths = [sorted_path_dict["path"] for sorted_path_dict in sorted_path_dicts]
        return sorted_paths

    def get_dir_name_keys(self):
        return self.dir_name_keys

    def get_info_which_todo_have(self, todo_file_path) -> dict:
        """
        TODOファイルの情報を返すメソッド

        Parameters
        ----------
        todo_file_path: str
            todoファイルのパス

        Returns
        -------
        todo_information: dict
            todoファイルに関する情報
        """
        metadata_list: list = self.search_meta_data(todo_file_path)
        todo_file_name: str = todo_file_path.split("\\")[-1].split(".")[0]

        todo_information: dict = {
            "metadata_list": metadata_list,
            "file_name": todo_file_name
        }

        return todo_information

    @staticmethod
    def get_contents_to_display_which_todo_have(todo_information) -> str:
        """
        Listboxへ表示するtodo名、メタデータ名を作成し返す関数

        Parameters
        ----------
        todo_information: dict
            todoに関する情報を格納したディクショナリ

        Returns
        -------
        " ".join(flatten(content_list)): str
            Listboxへ表示する文字列（todo名、メタデータ名を含む）
        """

        content_list = [
            re.sub(r"\[.*\]", "", todo_information["file_name"]),
            todo_information["metadata_list"],
        ]

        return " ".join(flatten(content_list))

    @staticmethod
    def get_todo_timestamp(path: str) -> Tuple[str, str]:
        """
        TODOファイルが作成・更新されたタイムスタンプを取得するメソッド

        Parameters
        -----------
        path: str
            TODOファイルのパス

        Returns
        -------
        create_time, update_time: Tuple[str, str]
            作成日時と更新日時
        """
        stat_result = os.stat(path)
        create_time = datetime.datetime.fromtimestamp(stat_result.st_ctime).strftime("%Y/%m/%d %H:%M:%S")
        update_time = datetime.datetime.fromtimestamp(stat_result.st_mtime).strftime("%Y/%m/%d %H:%M:%S")

        return create_time, update_time

    @staticmethod
    def get_todo_detail(path: str) -> str:
        """
        TODOファイルの詳細情報を取得するメソッド

        Parameters
        -----------
        path: str
            TODOファイルのパス

        Returns
        --------
        f.read(): str
            詳細情報
        """
        try:
            with open(path, encoding="utf_8") as f:
                return f.read()
        except UnicodeDecodeError:
            return "このファイルはプレビューできません。"

    @staticmethod
    def close_todo(todo_path: str) -> None:
        """
        TODOファイルをクローズするメソッド
        Parameters
        ----------
        todo_path: str
            TODOファイルのパス

        Returns
        -------
        None
        """
        os.rename(todo_path,
                  os.path.join(
                      os.path.dirname(todo_path), os.path.basename(todo_path).replace("todo", "完了"))
                  )

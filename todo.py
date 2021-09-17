from operate_file_1 import get_all_files
import configparser
import re
import linecache
import os
import datetime
import hashlib


class Todo:
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
        paths = []
        for dir_name in self.dir_names:
            paths.extend(list(get_all_files(dir_name, ";".join(self.patterns))))
        return paths

    def limit_search_file(self, dir_name_key):
        paths = list(get_all_files(self.rule_file["Dir_names"][dir_name_key], ";".join(self.patterns)))
        return paths

    def search_importance(self, file_name):
        result = self.judge_importance(file_name)
        if result is None:
            return self.rule_file["Importance_color"]["default"]
        else:
            return self.rule_file["Importance_color"][result.group()[1]]

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
                if metadata != "":
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

    def sort_importance(self, paths):
        path_dicts = []
        for path in paths:
            path_dict = {}
            file_name = path.split("\\")[-1].split(".")[0]
            result = self.judge_importance(file_name)
            if result is None:
                path_dict["importance"] = "z"
            else:
                path_dict["importance"] = result.group()[1]
            path_dict["path"] = path
            path_dicts.append(path_dict)

        sorted_path_dicts = sorted(path_dicts, key=lambda x: x["importance"])
        sorted_paths = [sorted_path_dict["path"] for sorted_path_dict in sorted_path_dicts]
        return sorted_paths

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

    def judge_importance(self, file_name):
        pattern = r"\[[{0}]\]".format(
            "|".join(
                [key.upper() for key in self.rule_file["Importance_color"].keys()]
            )
        )
        re_pattern = re.compile(pattern)
        result = re_pattern.search(file_name)
        return result

    def get_dir_name_keys(self):
        return self.dir_name_keys

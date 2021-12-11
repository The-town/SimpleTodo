from tkinter import *
from tkinter import messagebox
from tkinter import filedialog, simpledialog
import tkinter as tk
from typing import Tuple

from todo import Todo
from gui_object import Frame, Label, Listbox, TextForDisplayDetail, Button, Combobox, DialogForAddTodo, CloseTodoButton
from flatten import flatten
import re
import os
import datetime


class TodoDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("todo")
        self.root.configure(background='white')

        self.todo = Todo()
        self.todo_list_box_dict = {}

        self.todo_list_frame = Frame(self.root)
        self.todo_list_frame.grid(column=0, row=1)
        self.todo_detail_frame = Frame(self.root)
        self.todo_detail_frame.grid(column=1, row=1)
        self.function_frame = Frame(self.root)
        self.function_frame.grid(column=0, columnspan=2, row=0)

        self.todo_listbox = Listbox(master=self.todo_list_frame, master_of_detail_text=self.todo_detail_frame)
        self.todo_listbox.bind("<Button-1>", self.display_todo_detail)
        self.todo_listbox.bind("<Return>", self.display_todo_detail)

        self.add_todo_button = Button(master=self.function_frame)
        self.add_todo_button.grid(column=5, row=0, padx=5)
        self.add_todo_button["text"] = "TODO追加"
        self.add_todo_button["command"] = self.add_todo

        self.refresh_button = Button(master=self.function_frame)
        self.refresh_button.grid(column=4, row=0, padx=5)
        self.refresh_button["text"] = "更新"
        self.refresh_button["command"] = self.refresh

        self.sort_label: Label = Label(master=self.function_frame)
        self.sort_label["text"] = "フィルタ"
        self.sort_label.grid(column=2, row=0)

        self.dir_combbox = Combobox(master=self.function_frame)
        self.dir_combbox.grid(column=3, row=0, padx=(0,100))
        self.set_value_for_dir_combbox()

        self.sort_label: Label = Label(master=self.function_frame)
        self.sort_label["text"] = "ソート方法"
        self.sort_label.grid(column=0, row=0)

        self.sort_combbox = Combobox(master=self.function_frame)
        self.sort_combbox.grid(column=1, row=0, padx=(0, 100))
        self.set_value_for_sort_combbox()

    def display_todo(self):
        todo_list_box_id = 0
        self.todo_list_box_dict = {}
        paths = self.get_paths_which_todo_file_have()

        for path in paths:
            todo_information = self.get_info_which_todo_have(path)
            contents_to_display = self.get_contents_to_display_which_todo_have(todo_information)
            self.todo_listbox.insert(todo_list_box_id, contents_to_display)

            importance_color = self.todo.search_importance(todo_information["file_name"])
            self.todo_listbox.itemconfig(todo_list_box_id, {'bg': importance_color})

            self.todo_list_box_dict[todo_list_box_id] = path
            todo_list_box_id = todo_list_box_id + 1

        self.todo_listbox.set_todo_list(self.todo_list_box_dict)

    def display_todo_detail(self, event=None) -> None:
        if str(event.type) == "ButtonPress":
            self.todo_listbox.activate_line_clicked(event=event)

        self.todo_listbox.text.destroy()

        todo_path: str = self.todo_listbox.todo_list[self.todo_listbox.index(ACTIVE)]
        self.todo_listbox.text = TextForDisplayDetail(self.todo_listbox.master_of_detail_text)

        self.todo_listbox.text.tag_bind("system_message_file_path", "<Double-Button-1>",
                                        self.todo_listbox.open_with_another_app)
        self.todo_listbox.text.tag_bind("system_message_folder_path", "<Double-Button-1>",
                                        self.todo_listbox.open_folder)
        create_time, update_time = self.get_todo_timestamp(todo_path)
        self.todo_listbox.text.insert(END, "ファイルを開く", "system_message_file_path")
        self.todo_listbox.text.insert(END, "\t\t")
        self.todo_listbox.text.insert(END, "フォルダを開く", "system_message_folder_path")
        self.todo_listbox.text.insert(END, "\n\n")
        self.todo_listbox.text.insert(END, self.get_todo_detail(todo_path))

        self.todo_listbox.text.insert(END, "\n\n======メタデータ======\n\n")
        self.todo_listbox.text.insert(END, "作成 {0} 更新 {1}".format(create_time, update_time))
        self.todo_listbox.text.insert(END, "\n")
        self.todo_listbox.text.insert(END, todo_path)

        self.todo_listbox.text.insert(END, "\n\n======TODO操作======\n\n")
        close_todo_button = CloseTodoButton()
        close_todo_button["command"] = self.todo_listbox.close_todo
        self.todo_listbox.text.window_create(tk.END, window=close_todo_button)

        self.todo_listbox.text.grid(column=0, row=1, columnspan=3)

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

    def get_paths_which_todo_file_have(self):
        paths = self.todo.get_paths_which_result_of_search(self.dir_combbox.get())
        sorted_paths = self.todo.sort_todo(paths, method=self.sort_combbox.get())

        return sorted_paths

    def get_info_which_todo_have(self, todo_file_path):
        metadata_list = self.todo.search_meta_data(todo_file_path)
        todo_file_name = todo_file_path.split("\\")[-1].split(".")[0]

        todo_information = {
            "metadata_list": metadata_list,
            "file_name": todo_file_name
        }

        return todo_information

    def get_contents_to_display_which_todo_have(self, todo_information) -> str:
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

    def refresh(self, event=None):
        self.todo_listbox.delete(0, "end")
        self.display_todo()

    def add_todo(self, event=None):
        """
        todoファイルを追加するためにDialogオブジェクトを呼び出す。

        Parameters
        ----------
        event:

        Returns
        -------
        None
        """
        dir_names_items: dict = self.todo.dir_names_items
        DialogForAddTodo(self.root, items_for_combobox=dir_names_items)

    def set_value_for_dir_combbox(self):
        self.dir_combbox["value"] = ["all"] + self.todo.get_dir_name_keys()

    def set_value_for_sort_combbox(self):
        self.sort_combbox["value"] = ["重要度", "期限"]

    def mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    todo_display = TodoDisplay()
    todo_display.display_todo()
    todo_display.mainloop()

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog, simpledialog
import tkinter as tk
from todo import Todo
from gui_object import Frame, Label, Listbox, Text, Button, Combobox, DialogForAddTodo
from flatten import flatten
import re


class TodoDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("todo")

        self.todo = Todo()
        self.todo_list_box_dict = {}

        self.todo_list_frame = Frame(self.root)
        self.todo_list_frame.grid(column=0, row=1)
        self.todo_detail_frame = Frame(self.root)
        self.todo_detail_frame.grid(column=1, row=1)
        self.function_frame = Frame(self.root)
        self.function_frame.grid(column=0, columnspan=2, row=0)

        self.listbox = Listbox(master=self.todo_list_frame, master_of_detail_text=self.todo_detail_frame)

        self.add_todo_button = Button(master=self.function_frame)
        self.add_todo_button.grid(column=3, row=0)
        self.add_todo_button["text"] = "TODO追加"
        self.add_todo_button["command"] = self.add_todo

        self.refresh_button = Button(master=self.function_frame)
        self.refresh_button.grid(column=2, row=0)
        self.refresh_button["text"] = "更新"
        self.refresh_button["command"] = self.refresh

        self.dir_combbox = Combobox(master=self.function_frame)
        self.dir_combbox.grid(column=1, row=0, padx=(0,100))
        self.set_value_for_dir_combbox()

        self.sort_combbox = Combobox(master=self.function_frame)
        self.sort_combbox.grid(column=0, row=0, padx=(0, 100))
        self.set_value_for_sort_combbox()

    def display_todo(self):
        todo_list_box_id = 0
        self.todo_list_box_dict = {}
        paths = self.get_paths_which_todo_file_have()

        for path in paths:
            todo_information = self.get_info_which_todo_have(path)
            contents_to_display = self.get_contents_to_display_which_todo_have(todo_information)
            self.listbox.insert(todo_list_box_id, contents_to_display)

            importance_color = self.todo.search_importance(todo_information["file_name"])
            self.listbox.itemconfig(todo_list_box_id, {'bg': importance_color})

            self.todo_list_box_dict[todo_list_box_id] = path
            todo_list_box_id = todo_list_box_id + 1

        self.listbox.set_todo_list(self.todo_list_box_dict)

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
        self.listbox.delete(0, "end")
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
        self.sort_combbox["value"] = ["importance", "limit"]

    def mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    todo_display = TodoDisplay()
    todo_display.display_todo()
    todo_display.mainloop()

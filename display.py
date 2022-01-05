from tkinter import *
import tkinter as tk
from typing import List

from todo import ControlTodo, Todo
from gui_object import Frame, Label, Listbox, TextForDisplayDetail, Button, Combobox, DialogForAddTodo, \
    DialogConfirmForCloseTodo, DialogForUpdateTodo, CloseTodoButton
import os
import subprocess


class TodoDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("todo")
        self.root.configure(background='white')

        self.control_todo = ControlTodo()

        self.function_frame = Frame(self.root)
        self.function_frame.grid(column=0, columnspan=2, row=0)

        self.add_todo_button = Button(master=self.function_frame)
        self.add_todo_button.grid(column=5, row=0, padx=5)
        self.add_todo_button["text"] = "追加"
        self.add_todo_button["command"] = self.add_todo

        self.close_todo_button = CloseTodoButton(self.function_frame)
        self.close_todo_button.grid(column=6, row=0, padx=5)
        self.close_todo_button["command"] = self.close_todo

        self.update_todo_button = Button(self.function_frame)
        self.update_todo_button.grid(column=7, row=0, padx=5)
        self.update_todo_button["text"] = "編集"
        self.update_todo_button["command"] = self.update_todo

        self.refresh_button = Button(master=self.function_frame)
        self.refresh_button.grid(column=4, row=0, padx=5)
        self.refresh_button["text"] = "更新"
        self.refresh_button["command"] = self.refresh

        self.sort_label: Label = Label(master=self.function_frame)
        self.sort_label["text"] = "フィルタ"
        self.sort_label.grid(column=0, row=1)

        self.dir_combobox = Combobox(master=self.function_frame)
        self.dir_combobox.grid(column=1, row=1, padx=(0, 100))
        self.set_value_for_dir_combobox()

        self.sort_label: Label = Label(master=self.function_frame)
        self.sort_label["text"] = "ソート方法"
        self.sort_label.grid(column=0, row=0)

        self.sort_combobox = Combobox(master=self.function_frame)
        self.sort_combobox.grid(column=1, row=0, padx=(0, 100))
        self.set_value_for_sort_combobox()

        self.todo_display_list: TodoListDisplay = TodoListDisplay(master=self.root, control_todo=self.control_todo)
        self.todo_display_list.display_todo_list(self.dir_combobox.get(), self.sort_combobox.get())

    def refresh(self, event=None):
        self.todo_display_list: TodoListDisplay = TodoListDisplay(master=self.root, control_todo=self.control_todo)
        self.todo_display_list.display_todo_list(self.dir_combobox.get(), self.sort_combobox.get())

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
        dir_names_items: dict = self.control_todo.dir_names_items
        DialogForAddTodo(self.root, items_for_combobox=dir_names_items)
        self.refresh()

    def update_todo(self, event=None) -> None:
        todo: Todo = self.todo_display_list.todo_list_box_dict[self.todo_display_list.todo_listbox.index(ACTIVE)]
        DialogForUpdateTodo(self.root, todo)
        self.refresh()

    def close_todo(self, event=None) -> None:
        """
        todoファイルを完了にする。

        Parameters
        ----------
        event

        Returns
        -------
        None
        """
        todo: Todo = self.todo_display_list.todo_list_box_dict[self.todo_display_list.todo_listbox.index(ACTIVE)]
        DialogConfirmForCloseTodo(self.root, self.control_todo, todo)
        self.refresh()

    def set_value_for_dir_combobox(self):
        self.dir_combobox["value"] = ["all"] + self.control_todo.get_dir_name_keys()
        self.dir_combobox.current(0)

    def set_value_for_sort_combobox(self):
        self.sort_combobox["value"] = ["重要度", "期限"]
        self.sort_combobox.current(1)

    def mainloop(self):
        self.root.mainloop()


class TodoListDisplay:
    def __init__(self, master, control_todo: ControlTodo) -> None:
        self.master = master
        todo_list_frame = Frame(self.master)
        todo_list_frame.grid(column=0, row=1)

        self.todo_listbox = Listbox(master=todo_list_frame)
        self.todo_listbox.bind("<Button-1>", self.display_todo_detail)
        self.todo_listbox.bind("<Return>", self.display_todo_detail)

        self.control_todo: ControlTodo = control_todo
        self.todo_list_box_dict: dict = {}

    def display_todo_list(self, todo_directory: str, sort_method: str) -> None:
        todo_list_box_id = 0
        self.todo_list_box_dict = {}
        todos: List[Todo] = self.get_paths_which_todo_file_have(self.control_todo, todo_directory, sort_method)

        for todo in todos:
            self.todo_listbox.insert(todo_list_box_id, self.control_todo.get_content_todo_for_display_list(todo))
            self.todo_listbox.itemconfig(todo_list_box_id, {'bg': todo.importance_color})
            self.todo_list_box_dict[todo_list_box_id] = todo
            todo_list_box_id = todo_list_box_id + 1

    def display_todo_detail(self, event=None) -> None:
        if str(event.type) == "ButtonPress":
            self.todo_listbox.activate_line_clicked(event=event)

        todo: Todo = self.todo_list_box_dict[self.todo_listbox.index(ACTIVE)]
        todo_detail: TodoDetailDisplay = TodoDetailDisplay(todo, self.control_todo, self.master)
        todo_detail.display_todo_detail()

    @staticmethod
    def get_paths_which_todo_file_have(control_todo: ControlTodo, directory: str, sort_method: str):
        todos: List[Todo] = control_todo.get_paths_which_result_of_search(directory)
        sorted_todos: List[Todo] = control_todo.sort_todo(todos, method=sort_method)

        return sorted_todos


class TodoDetailDisplay:
    def __init__(self, todo: Todo, control_todo: ControlTodo, master=None) -> None:
        self.todo_detail_frame = Frame(master)
        self.todo_detail_frame.grid(column=1, row=1)

        self.control_todo: ControlTodo = control_todo
        self.todo: Todo = todo

    def display_todo_detail(self) -> None:
        text = TextForDisplayDetail(self.todo_detail_frame)

        text.tag_bind("system_message_file_path", "<Double-Button-1>", self.open_with_another_app)
        text.tag_bind("system_message_folder_path", "<Double-Button-1>", self.open_folder)
        text.insert(END, "ファイルを開く", "system_message_file_path")
        text.insert(END, "\t\t")
        text.insert(END, "フォルダを開く", "system_message_folder_path")
        text.insert(END, "\n\n")
        text.insert(END, self.todo.detail)

        text.insert(END, "\n\n======メタデータ======\n\n")
        text.insert(END, "作成 {0} 更新 {1}".format(self.todo.create_time, self.todo.update_time))
        text.insert(END, "\n")
        text.insert(END, self.todo.path)

        text.grid(column=0, row=1, columnspan=3)

    def open_with_another_app(self, event=None):
        os.system("start " + self.todo.path)

    def open_folder(self, event=None):
        subprocess.run("explorer {0}".format(os.path.dirname(self.todo.path)))


if __name__ == "__main__":
    todo_display = TodoDisplay()
    todo_display.root.mainloop()


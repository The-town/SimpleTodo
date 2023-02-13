import webbrowser
from tkinter import *
import tkinter as tk
from typing import List

from todo import ControlTodo, Todo
from gui_object import Frame, Listbox, TextForDisplayDetail, DialogForAddTodo, \
    DialogConfirmForCloseTodo, DialogForUpdateTodo, RightClickMenu
import os
import subprocess


class TodoDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("todo")
        self.root.configure(background='white')

        self.control_todo = ControlTodo()

        self.todo_frame: Frame = Frame(self.root)
        self.todo_frame.pack(side="bottom", fill="both", expand=True)

        self.right_click_menu: RightClickMenu = RightClickMenu(self.root)
        self.dir_name_var: StringVar = StringVar()

        self.right_click_menu.set_value_for_select_dir_menu(self.dir_name_var, self.control_todo, self.refresh)
        self.right_click_menu.set_value_for_control_todo_menu(self.update_todo, self.add_todo, self.close_todo)
        self.right_click_menu.set_value_for_select_sort_menu(self.sort_todo_with_limit, self.sort_todo_with_importance)

        self.todo_display_list: TodoListDisplay = TodoListDisplay(master=self.todo_frame, control_todo=self.control_todo)
        self.todo_display_list.display_todo_list(self.dir_name_var.get())

    def refresh(self, event=None, index_todo_list: int = 0):
        self.todo_display_list.todo_listbox.activate(index_todo_list)
        self.todo_display_list.display_todo_list(self.dir_name_var.get(), activate_index=index_todo_list)

    def auto_refresh(self) -> None:
        """
        TODOのリストを定期的に更新するメソッド
        """
        index: int = 0
        if len(self.todo_display_list.todo_listbox.curselection()) > 0:
            index: int = self.todo_display_list.todo_listbox.curselection()[0]
        self.refresh(index_todo_list=index)
        self.root.after(10000, self.auto_refresh)

    def sort_todo_with_limit(self, event=None):
        self.todo_display_list.display_todo_list(self.dir_name_var.get(), "期限")

    def sort_todo_with_importance(self, event=None):
        self.todo_display_list.display_todo_list(self.dir_name_var.get(), "重要度")

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
        DialogForAddTodo(self.root, dir_names_items, self.dir_name_var.get())
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

    def mainloop(self):
        self.root.mainloop()


class TodoListDisplay:
    def __init__(self, master, control_todo: ControlTodo) -> None:
        self.master = master
        todo_list_frame = Frame(self.master)
        todo_list_frame.pack(side="left", fill="both", expand=True)

        self.todo_listbox = Listbox(master=todo_list_frame)
        self.todo_listbox.bind("<Button-1>", self.display_todo_detail)
        self.todo_listbox.bind("<Return>", self.display_todo_detail)

        self.control_todo: ControlTodo = control_todo
        self.todo_list_box_dict: dict = {}

        self.todo_detail: TodoDetailDisplay = TodoDetailDisplay(master=self.master)

    def display_todo_list(self, todo_directory: str, sort_method: str = "期限", activate_index: int = 0) -> None:
        """
        TODOのリストを表示するメソッド

        Parameters
        ----------
        todo_directory: str
        sort_method: str
        activate_index: int
            デフォルトでアクティブ（選択状態）にするリストのインデックス

        Returns
        --------
        None
        """
        self.todo_listbox.delete(0, END)

        todo_list_box_id = 0
        self.todo_list_box_dict = {}
        todos: List[Todo] = self.get_paths_which_todo_file_have(self.control_todo, todo_directory, sort_method)

        for todo in todos:
            self.todo_listbox.insert(todo_list_box_id, self.control_todo.get_content_todo_for_display_list(todo))
            self.todo_listbox.itemconfig(todo_list_box_id, {'bg': todo.importance_color})
            self.todo_list_box_dict[todo_list_box_id] = todo
            todo_list_box_id = todo_list_box_id + 1

        self.todo_listbox.activate(activate_index)
        self.todo_listbox.selection_set(activate_index, last=None)

    def display_todo_detail(self, event=None) -> None:
        if str(event.type) == "ButtonPress":
            self.todo_listbox.activate_line_clicked(event=event)

        todo: Todo = self.todo_list_box_dict[self.todo_listbox.index(ACTIVE)]

        self.todo_detail.todo = todo
        self.todo_detail.control_todo = self.control_todo
        self.todo_detail.display_todo_detail()

    @staticmethod
    def get_paths_which_todo_file_have(control_todo: ControlTodo, directory: str, sort_method: str):
        todos: List[Todo] = control_todo.get_paths_which_result_of_search(directory)
        sorted_todos: List[Todo] = control_todo.sort_todo(todos, method=sort_method)

        return sorted_todos


class TodoDetailDisplay:
    def __init__(self, todo: Todo = None, control_todo: ControlTodo = None, master=None) -> None:
        self.todo_detail_frame = Frame(master)
        self.todo_detail_frame.pack(side="left", fill="both", expand=True)

        self.control_todo: ControlTodo = control_todo
        self.todo: Todo = todo

        self.detail_text: TextForDisplayDetail = TextForDisplayDetail(self.todo_detail_frame)
        self.detail_text.bind("<KeyPress>", self.save_todo)
        self.detail_text.bind("<KeyRelease>", self.save_todo)
        self.detail_text["height"] = 15

        self.metadata_text: TextForDisplayDetail = TextForDisplayDetail(self.todo_detail_frame)
        self.metadata_text["height"] = 5

        self.detail_text.pack(side="top", fill="both", expand=True)
        self.metadata_text.pack(side="bottom", fill="both", expand=True)

        self.detail_text.tag_bind("url", "<Double-Button-1>", self.open_url)

    def display_todo_detail(self) -> None:
        self.detail_text.delete(1.0, END)
        self.insert_detail_text()

        self.metadata_text["state"] = "normal"
        self.metadata_text.delete(1.0, END)
        self.metadata_text.tag_bind("system_message_file_path", "<Double-Button-1>", self.open_with_another_app)
        self.metadata_text.tag_bind("system_message_folder_path", "<Double-Button-1>", self.open_folder)
        self.metadata_text.insert(END, "ファイルを開く", "system_message_file_path")
        self.metadata_text.insert(END, "\t\t")
        self.metadata_text.insert(END, "フォルダを開く", "system_message_folder_path")
        self.metadata_text.insert(END, "\n\n")
        self.metadata_text.insert(END, "作成 {0} 更新 {1}".format(self.todo.create_time, self.todo.update_time))
        self.metadata_text.insert(END, "\n")
        self.metadata_text.insert(END, self.todo.path)
        self.metadata_text["state"] = "disabled"

        self.detail_text.edit_reset()
        self.metadata_text.edit_reset()  # 上記で挿入している文字列をundoで消去しないように、undo stackをリセットする

    def insert_detail_text(self) -> None:
        """
        TODO詳細内容をテキストへ挿入するメソッド

        Returns
        -------
        None
        """
        lines_with_url: tuple = self.get_lines_url()

        detail_text_list: list = self.todo.detail.split("\n")
        for line, detail_text in enumerate(detail_text_list):
            if line in lines_with_url:
                self.detail_text.insert(END, detail_text + "\n", "url")
            else:
                self.detail_text.insert(END, detail_text + "\n")

    def open_with_another_app(self, event=None):
        os.system("start " + self.todo.path)

    def open_folder(self, event=None):
        subprocess.run("explorer {0}".format(os.path.dirname(self.todo.path)))

    def save_todo(self, event=None):
        """
        todo詳細画面に入力された文字列をファイルへ保存するためのメソッド

        Parameters
        ----------
        event

        Returns
        --------
        None
        """
        start_line: str = "1.0"
        end_line: str = "end"
        self.todo.detail = self.detail_text.get(start_line, end_line)[:-1]  # getをした際に、改行文字列が入るため除去
        self.control_todo.save_todo(self.todo)

    def get_lines_url(self) -> tuple:
        """
        URLが記載されている行数を返すメソッド

        Returns
        --------
        lines_with_url: tuple
            urlが書かれている行数
        """
        detail_text_list: list = self.todo.detail.split("\n")
        lines_with_url: list = []
        for line, detail_text in enumerate(detail_text_list):
            if re.search(r"^https?://", detail_text):
                lines_with_url.append(line)

        return tuple(lines_with_url)

    def open_url(self, event=None) -> None:
        """
        URLをブラウザで開くメソッド

        Parameters
        -----------
        event:

        Returns
        --------
        None
        """
        url: str = self.detail_text.get('insert linestart', 'insert lineend')
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    todo_display = TodoDisplay()
    todo_display.auto_refresh()
    todo_display.root.mainloop()


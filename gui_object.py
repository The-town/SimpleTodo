from tkinter import *
from tkinter import simpledialog
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
import os
import configparser
from validate import validate_todo_name, validate_double_todo_name
from todo import Todo, ControlTodo


class Frame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(column=0, row=0)
        self["width"] = 100
        self["height"] = 100
        self["padx"] = 10
        self["pady"] = 10
        self["bg"] = "white"


class Label(tk.Label):
    def __init__(self, master=None):
        tk.Label.__init__(self, master)

        self["font"] = ("メイリオ", 15)
        self["width"] = 10
        self["bg"] = "white"


class Button(tk.Button):
    def __init__(self, master=None):
        tk.Button.__init__(self, master)

        self["height"] = 1
        self["width"] = 10
        self["font"] = ("メイリオ", 15)


class CloseTodoButton(tk.Button):
    def __init__(self, master=None):
        tk.Button.__init__(self, master)

        self["height"] = 1
        self["width"] = 10
        self["font"] = ("メイリオ", 15)
        self["text"] = "完了"


class RefreshButton(Button):
    def __init__(self, master=None,):
        Button.__init__(self, master)


class Combobox(ttk.Combobox):
    def __init__(self, master=None):
        ttk.Combobox.__init__(self, master)

        self["font"] = ("メイリオ", 15)


class Text(scrolledtext.ScrolledText):
    def __init__(self, master=None):
        scrolledtext.ScrolledText.__init__(self, master)
        self["width"] = 50
        self["height"] = 20
        self["font"] = ("メイリオ", 12)


class Entry(ttk.Entry):
    def __init__(self, master=None):
        ttk.Entry.__init__(self, master)

        self["font"] = ("メイリオ", 11)
        self["width"] = 25


class TextForDisplayDetail(Text):
    def __init__(self, master=None):
        Text.__init__(self, master)

        self.tag_config('system_message_file_path', background="white", foreground="blue", underline=1)
        self.tag_config('system_message_folder_path', background="white", foreground="blue", underline=1)


class Listbox(tk.Listbox):
    def __init__(self, master=None):
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)
        tk.Listbox.__init__(self, master, yscrollcommand=scrollbar.set, selectmode=EXTENDED)

        self.pack(side=LEFT, fill=BOTH)
        self["width"] = 50
        self["height"] = 20
        self["font"] = ("メイリオ", 12)
        self.master = master

        scrollbar["command"] = self.yview

        self.todo_list = {}

    # 選択された行をactive状態にするメソッド
    # シングルクリックの場合にactive状態へ遷移させるために実装した
    def activate_line_clicked(self, event=None):
        self.selection_clear(0, tk.END)
        self.selection_set(self.nearest(event.y))
        self.activate(self.nearest(event.y))


class CustomizeSimpleDialog(simpledialog.Dialog):
    """
    ダイアログの背景色を白にするためにオーバーライド
    デフォルトは白。
    """
    def __init__(self, master, title=None, bg_color="white") -> None:
        parent = master

        '''
        ダイアログの初期化
        背景色を変えるためにオーバーライドしている。
        '''
        Toplevel.__init__(self, parent, bg=bg_color)  # 背景色の変更

        self.withdraw()  # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                      parent.winfo_rooty() + 50))

        self.deiconify()  # become visible now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def buttonbox(self):
        """
        OKとCancelボタンを作成するためのメソッド。
        ボタンの色を変更するためにオーバーライドしている。

        Parameters
        ----------

        Returns
        -------
        None
        """

        box = tk.Frame(self)
        box["bg"] = "white"

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()


class DialogConfirmForCloseTodo(CustomizeSimpleDialog):
    """
    TODOを完了状態にする
    """
    def __init__(self, master, control_todo: ControlTodo, todo: Todo):

        self.control_todo: ControlTodo = control_todo
        self.todo: Todo = todo

        super().__init__(master)

    def body(self, master):
        """
        Dialogオブジェクトへ配置するオブジェクトを定義する。
        完了にするTODOオブジェクトの情報を確認する

        Parameters
        ----------
        master:
            Dialogオブジェクトの親オブジェクト

        Returns
        -------
        None
        """
        close_message_label: Label = Label(master)
        close_message_label["text"] = "以下のTODOを完了にします。"
        close_message_label["width"] = 30
        close_message_label.grid(column=0, row=0)

        todo_info_text: Text = Text(master)
        todo_info_text.insert(END, self.todo.name)
        todo_info_text.insert(END, "\n\n")
        todo_info_text.insert(END, self.todo.detail)
        todo_info_text["height"] = 10
        todo_info_text.grid(column=0, row=1)

    def apply(self):
        """
        このDialogオブジェクトが破棄される際に実行される処理を定義する。
        対象のTODOファイルを完了状態にする。

        Parameters
        ----------

        Returns
        -------
        None
        """
        self.control_todo.close_todo(self.todo)


class DialogForAddTodo(simpledialog.Dialog):
    def __init__(self, master, items_for_combobox, title=None) -> None:
        self.items_for_combobox: dict = items_for_combobox
        parent = master

        self.rule_file = configparser.ConfigParser()
        self.rule_file.read("./config.ini", "UTF-8")

        '''
        ダイアログの初期化
        背景色を変えるためにオーバーライドしている。
        '''
        Toplevel.__init__(self, parent, bg="white")  # 背景色の変更

        self.withdraw()  # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                      parent.winfo_rooty()+50))

        self.deiconify() # become visible now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def buttonbox(self):
        """
        OKボタンにbindされているキーをReturnからControl-Returnへ変更するためにオーバーライドした。
        ダイアログの中でTextウィジェットを使っており、改行のためにReturnキーを使用するため
        """
        super().buttonbox()

        self.bind("<Control-Return>", self.ok)
        self.unbind("<Return>")

    def body(self, master) -> None:
        """
        Dialogオブジェクトへ配置するオブジェクトを定義する。
        Todoを追加するためにユーザーが入力する情報を受け取るための、GUIオブジェクトを作成している。

        Parameters
        ----------
        master:
            Dialogオブジェクトの親オブジェクト

        Returns
        -------
        None
        """

        description_combobox_label: Label = Label(master)
        description_combobox_label["text"] = "カテゴリを選択"
        description_combobox_label["width"] = 25
        description_combobox_label["fg"] = "black"
        description_combobox_label["bg"] = "white"
        description_combobox_label.grid(column=0, row=0)

        self.category: Combobox = Combobox(master)
        self.category["font"] = ("メイリオ", 11)
        self.category["value"] = list(self.items_for_combobox.keys())
        self.category.grid(column=1, row=0)

        description_entry_label: Label = Label(master)
        description_entry_label["text"] = "追加するTODO名を入力"
        description_entry_label["width"] = 25
        description_entry_label["fg"] = "black"
        description_entry_label["bg"] = "white"
        description_entry_label.grid(column=0, row=1)

        self.todo_name: Entry = Entry(master)
        self.todo_name.grid(column=1, row=1)

        todo_detail_label: Label = Label(master)
        todo_detail_label["text"] = "TODOの詳細内容を入力"
        todo_detail_label["width"] = 25
        todo_detail_label["fg"] = "black"
        todo_detail_label["bg"] = "white"
        todo_detail_label.grid(column=0, row=2)

        self.todo_detail_text: Text = Text(master)
        self.todo_detail_text["width"] = 30
        self.todo_detail_text["height"] = 5
        self.todo_detail_text.grid(column=1, row=2)

        self.todo_name_check_message: Message = tk.Message(master)
        self.todo_name_check_message["aspect"] = 300
        self.todo_name_check_message["font"] = ("メイリオ", 9)
        self.todo_name_check_message["fg"] = "red"
        self.todo_name_check_message["bg"] = "white"

    def apply(self):
        """
        このDialogオブジェクトが破棄される際に実行される処理を定義する。
        ユーザーが入力した情報をもとに、TODOファイルを指定されたディレクトリへ作成する。

        Parameters
        ----------

        Returns
        -------
        None
        """
        todo_file_name: str = "".join([self.rule_file["string_when_add_todo"]["head"],
                                       self.todo_name.get(),
                                       self.rule_file["string_when_add_todo"]["tail"]])
        with open(os.path.join(self.items_for_combobox[self.category.get()], todo_file_name), "w", encoding="utf_8") \
                as f:
            f.write(self.todo_detail_text.get(1.0, END))

    def validate(self) -> bool:
        """
        このDialogオブジェクトが破棄される際に行う検証を定義する。
        todo名のバリデーションチェックを行う。

        Parameters
        ----------

        Returns
        -------
        None
        """
        todo_path: str = self.items_for_combobox[self.category.get()]
        todo_name: str = self.todo_name.get()
        todo_file_name: str = "".join([self.rule_file["string_when_add_todo"]["head"],
                                       todo_name,
                                       self.rule_file["string_when_add_todo"]["tail"]])

        is_validate_name, error_msg_name = validate_todo_name(todo_name)
        is_validate_double_name, error_msg_double_name = validate_double_todo_name(todo_file_name, todo_path)

        is_validate: bool = is_validate_name and is_validate_double_name
        error_msg: str = "\n".join([error_msg_name, error_msg_double_name])

        if is_validate:
            return True
        else:
            self.todo_name_check_message.grid(column=1, row=2)
            self.todo_name_check_message["text"] = error_msg
            return False

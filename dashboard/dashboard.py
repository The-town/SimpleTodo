from typing import List, Tuple, Dict
from todo import ControlTodo

import abc
import tkinter
import tkinter.ttk as ttk
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dar
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class DashboardRootWindow:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.geometry("600x600")
        self.root.configure(fg_color="#B4656F")


class ICounterForTodo(metaclass=abc.ABCMeta):
    """
    ダッシュボード上で何らかの数値を表示する
    """
    @abc.abstractmethod
    def get_todo_state(self) -> tuple:
        raise NotImplementedError()

    @abc.abstractmethod
    def sum_number_of_todo(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def display(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_label(self) -> customtkinter.CTkLabel:
        raise NotImplementedError()


class CounterForLimitWeekTodo(ICounterForTodo):
    """
    1週間後が期限のTODO数を表示するカウンター
    """
    def __init__(self, dashboard_root: DashboardRootWindow, name: str):
        self.dashboard_root: DashboardRootWindow = dashboard_root
        self.counter_var: tkinter.StringVar = tkinter.StringVar(master=self.dashboard_root.root)
        self.name: str = name

    def get_todo_state(self) -> tuple:
        """
        今週期限のTODOを取得するメソッド

        Returns
        --------
        todos: tuple
        """
        control_todo: ControlTodo = ControlTodo()
        todos = tuple(control_todo.search_file_until_spec_date(7))

        return todos

    def sum_number_of_todo(self) -> int:
        """
        TODOの数を合計するメソッド

        Returns
        --------
        number_of_active: int
        """
        todos: tuple = self.get_todo_state()
        number_of_active: int = len(todos)
        return number_of_active

    def display(self) -> None:
        """
        TODO数を表示するメソッド

        Returns
        --------
        None
        """
        number_of_active: int = self.sum_number_of_todo()
        self.counter_var.set(": ".join([self.name, str(number_of_active)]))

    def create_label(self) -> customtkinter.CTkLabel:
        """
        ダッシュボード用にラベルを作るメソッド

        Returns
        -------
        counter_label: customtkinter.CtkLabel
        """
        counter_label: customtkinter.CTkLabel = customtkinter.CTkLabel(
            self.dashboard_root.root,
            font=("メイリオ", 26),
            fg_color=("#B5CBB7", "gray"),
            text_color="black",
            textvariable=self.counter_var,
            height=300,
            width=300,
            wraplength=250
        )

        return counter_label


class CounterForActiveTodo(ICounterForTodo):
    """
    ダッシュボード上でアクティブなTODO数を表示する
    """
    def __init__(self, dashboard_root: DashboardRootWindow, name: str):
        self.dashboard_root: DashboardRootWindow = dashboard_root
        self.counter_var: tkinter.StringVar = tkinter.StringVar(master=self.dashboard_root.root)
        self.name: str = name

    def get_todo_state(self) -> tuple:
        """
        TODOの状態を取得するメソッド

        Returns
        --------
        todos: tuple
        """

        control_todo: ControlTodo = ControlTodo()
        todos = tuple(control_todo.search_file())

        return todos

    def sum_number_of_todo(self) -> int:
        """
        アクティブなTODOの数を合計するメソッド

        Returns
        --------
        number_of_active: int
        """
        todos: tuple = self.get_todo_state()
        number_of_active: int = len(todos)
        return number_of_active

    def display(self) -> None:
        """
        アクティブなTODO数を表示するメソッド

        Returns
        --------
        None
        """
        number_of_active: int = self.sum_number_of_todo()
        self.counter_var.set(": ".join([self.name, str(number_of_active)]))

    def create_label(self) -> customtkinter.CTkLabel:
        """
        ダッシュボード用にラベルを作るメソッド

        Returns
        -------
        counter_label: customtkinter.CTkLabel
        """
        counter_label: customtkinter.CTkLabel = customtkinter.CTkLabel(
            self.dashboard_root.root,
            font=("メイリオ", 26),
            fg_color=("#464E47", "gray"),
            text_color="white",
            textvariable=self.counter_var,
            height=300,
            width=300,
            wraplength=250
        )
        return counter_label


class DashBoard:
    """
    ダッシュボードを表すクラス
    """
    def __init__(self, dashboard_root: DashboardRootWindow, name="ダッシュボード") -> None:
        super().__init__()
        self.root: customtkinter.CTk = dashboard_root.root
        self.root.title(name)

        self.counters: Dict[str: ICounterForTodo, ...] = {}

    def display(self) -> None:
        """
        ウィンドウを表示するメソッド

        Returns
        -------
        None
        """
        for row, counter in enumerate(self.counters.values()):
            self.create_counter_for_active_todo(counter, column=0, row=row)

        self.root.mainloop()

    def add_counter(self, name: str, counter: ICounterForTodo):
        self.counters[name] = counter

    def update_counter(self):
        for counter in self.counters.values():
            counter.display()

        self.root.after(1000, self.update_counter)

    @staticmethod
    def create_counter_for_active_todo(counter: ICounterForTodo, column: int, row: int):
        counter_label: customtkinter.CTkLabel = counter.create_label()
        counter_label.grid(column=column, row=row)


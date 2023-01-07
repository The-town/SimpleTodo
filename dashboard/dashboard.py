from typing import List, Tuple, Dict
from todo import ControlTodo

import abc
import tkinter
import tkinter.ttk as ttk


class DashboardRootWindow:
    def __init__(self):
        self.root = tkinter.Tk()


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
    def create_label(self) -> tkinter.Label:
        raise NotImplementedError()


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

    def create_label(self) -> tkinter.Label:
        """
        ダッシュボード用にラベルを作るメソッド

        Returns
        -------
        counter_label: tkinter.Label
        """
        counter_label: ttk.Label = ttk.Label(self.dashboard_root.root)
        counter_label["padding"] = "1c"
        counter_label["font"] = ("メイリオ", 26)
        counter_label["background"] = "green"
        counter_label["foreground"] = "white"
        counter_label["relief"] = "groove"
        counter_label["textvariable"] = self.counter_var

        return counter_label


class DashBoard:
    """
    ダッシュボードを表すクラス
    """
    def __init__(self, dashboard_root: DashboardRootWindow, name="ダッシュボード") -> None:
        super().__init__()
        self.root: tkinter.Tk = dashboard_root.root
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
        counter_label: tkinter.Label = counter.create_label()
        counter_label.grid(column=column, row=row)


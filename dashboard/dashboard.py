import abc
import tkinter


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


class CounterForActiveTodo(ICounterForTodo):
    """
    ダッシュボード上でアクティブなTODO数を表示する
    """
    def __init__(self):
        self.counter_var: tkinter.StringVar = tkinter.StringVar()

    def get_todo_state(self) -> tuple:
        """
        TODOの状態を取得するメソッド

        Returns
        --------
        todos: tuple
        """
        todos: tuple = ("active", "no_active", "active")
        return todos

    def sum_number_of_todo(self) -> int:
        """
        アクティブなTODOの数を合計するメソッド

        Returns
        --------
        number_of_active: int
        """
        todos = self.get_todo_state()
        number_of_active: int = len([todo for todo in todos if todo == "active"])
        return number_of_active

    def display(self) -> None:
        """
        アクティブなTODO数を表示するメソッド

        Returns
        --------
        None
        """
        number_of_active: int = self.sum_number_of_todo()
        self.counter_var.set(str(number_of_active))


class DashBoard:
    """
    ダッシュボードを表すクラス
    """
    def __init__(self, name="ダッシュボード") -> None:
        self.root = tkinter.Tk()
        self.root.title(name)

    def display(self) -> None:
        """
        ウィンドウを表示するメソッド

        Returns
        -------
        None
        """
        counter_active_todo: CounterForActiveTodo = CounterForActiveTodo()
        counter_active_todo.display()

        active_todo_label: tkinter.Label = tkinter.Label(self.root)
        active_todo_label["textvariable"] = counter_active_todo.counter_var
        active_todo_label.grid(column=0, row=0)

        self.root.mainloop()


if __name__ == "__main__":
    dashboard = DashBoard()
    dashboard.display()

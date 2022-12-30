from dashboard.dashboard import DashBoard, CounterForActiveTodo, DashboardRootWindow
from todo import ControlTodo


control_todo: ControlTodo = ControlTodo()
todos: tuple = tuple(control_todo.search_file())
limit_todos: tuple = tuple(control_todo.limit_search_file("TODOアプリ開発"))

dashboard_root_window: DashboardRootWindow = DashboardRootWindow()

counter1: CounterForActiveTodo = CounterForActiveTodo(dashboard_root=dashboard_root_window,
                                                      name="全てのTODO数", todos=todos)
counter2: CounterForActiveTodo = CounterForActiveTodo(dashboard_root=dashboard_root_window,
                                                      name="TODOアプリ開発のTODO数", todos=limit_todos)

dashboard = DashBoard(dashboard_root=dashboard_root_window)
dashboard.add_counter("counter1", counter1)
dashboard.add_counter("counter2", counter2)

dashboard.display()

from dashboard.dashboard import DashBoard, CounterForActiveTodo, CounterForLimitWeekTodo, DashboardRootWindow
from todo import ControlTodo

import sys
sys.path.append('../')


dashboard_root_window: DashboardRootWindow = DashboardRootWindow()

active_todo_counter: CounterForActiveTodo = CounterForActiveTodo(dashboard_root=dashboard_root_window,
                                                                 name="全てのTODO数")
due_until_1week_todo_counter: CounterForLimitWeekTodo = CounterForLimitWeekTodo(dashboard_root=dashboard_root_window,
                                                                                name="期限が1週間以内のTODO数")

dashboard = DashBoard(dashboard_root=dashboard_root_window)
dashboard.add_counter("active_todo_counter", active_todo_counter)
dashboard.add_counter("due_until_1week_todo_counter", due_until_1week_todo_counter)
dashboard.update_counter()
dashboard.display()

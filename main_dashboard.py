from dashboard.dashboard import DashBoard, CounterForActiveTodo, DashboardRootWindow
from todo import ControlTodo

import sys
sys.path.append('../')


dashboard_root_window: DashboardRootWindow = DashboardRootWindow()

counter1: CounterForActiveTodo = CounterForActiveTodo(dashboard_root=dashboard_root_window,
                                                      name="全てのTODO数")

dashboard = DashBoard(dashboard_root=dashboard_root_window)
dashboard.add_counter("counter1", counter1)
dashboard.update_counter()
dashboard.display()

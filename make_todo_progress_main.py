"""
    このコードはtodoにかけた時間を測定するために使用していたが、
    要件が変更となり、todoにかけた時間を測定しなくなった。
    そのため現在（2021/01/17）は使用していない。
"""

from make_todo_progress import MakeTodoProgress


def get_todo_progress(path):
    make_graph_todo_progress = MakeTodoProgress()

    make_graph_todo_progress.set_path_of_display_todo(path)
    todo_info = make_graph_todo_progress.get_todo_info()

    todo_start_time_series = todo_info.query("status == 'start'")["timestamp"]
    todo_stop_time_series = todo_info.query("status == 'stop'")["timestamp"]

    return make_graph_todo_progress.get_sum_of_delta_datetime_list(todo_start_time_series, todo_stop_time_series)

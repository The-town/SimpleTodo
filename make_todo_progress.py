"""
    このコードはtodoにかけた時間を測定するために使用していたが、
    要件が変更となり、todoにかけた時間を測定しなくなった。
    そのため現在（2021/01/17）は使用していない。
"""


import pandas as pd
import datetime
import hashlib
import os


class MakeTodoProgress:
    def __init__(self):
        self.info_of_todo = pd.read_csv("./info_of_todo.log",
                                        delimiter=" ",
                                        names=["hash", "path", "status", "year", "month", "day", "timestamp"])
        self.path_of_display_todo = ""
        self.delta_datetime_list = []

    def set_path_of_display_todo(self, path):
        self.path_of_display_todo = path

    def get_todo_info(self):
        return self.info_of_todo.query(
            "hash == '{0}'".format(
                hashlib.sha256(self.path_of_display_todo.encode()).hexdigest()
            )
        )

    def convert_series_to_datetime(self, series, date_time_format):
        list = series.to_list()
        date_time_list = [datetime.datetime.strptime(str(time), date_time_format) for time in list]
        return date_time_list

    def get_sum_of_delta_datetime_list(self, todo_start_time_series, todo_stop_time_series):
        todo_start_time_date_time = self.convert_series_to_datetime(todo_start_time_series, "%Y%m%d%H%M%S")
        todo_stop_time_date_time = self.convert_series_to_datetime(todo_stop_time_series, "%Y%m%d%H%M%S")
        self.delta_datetime_list = []

        for i in range(len(todo_stop_time_date_time)):
            self.delta_datetime_list.append(
                (todo_stop_time_date_time[i] - todo_start_time_date_time[i]).total_seconds()
            )

        return sum(self.delta_datetime_list)

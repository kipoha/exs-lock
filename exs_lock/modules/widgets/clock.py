from datetime import datetime

from fabric.core.fabricator import Fabricator
from fabric.widgets.label import Label
from fabric.widgets.box import Box

from exs_lock.utils.loop import run_in_thread


time_format = "%H:%M:%S"
date_format = "%d %B, %Y"


class DateTime(Box):
    __gtype_name__ = "ExsDateTime"

    def __init__(self):
        time, date = self.get_dt()
        hours, minutes, seconds = time.split(":")
        self.hours = Label(hours, name="lockscreen-hours")
        self.minutes = Label(minutes, name="lockscreen-minutes")
        self.seconds = Label(seconds, name="lockscreen-seconds")
        self.time = Box(
            0,
            "v",
            [
                self.hours,
                self.seconds,
                self.minutes,
            ],
            "lockscreen-time",
        )
        self.date = Label(date, name="lockscreen-date")
        super().__init__(
            10,
            "v",
            [
                self.time,
                self.date,
            ],
            "lockscreen-datetime",
            v_align="center",
            h_align="center",
        )
        self.run_fabricator()

    @run_in_thread
    def run_fabricator(self):
        Fabricator(poll_from=self.update)

    def update(self, _):
        time, date = self.get_dt()
        hours, minutes, seconds = time.split(":")
        self.hours.set_text(hours)
        self.minutes.set_text(minutes)
        self.seconds.set_text(seconds)
        self.date.set_text(date)

    def get_dt(self) -> tuple[str, str]:
        now = datetime.now()
        return now.strftime(time_format), now.strftime(date_format)

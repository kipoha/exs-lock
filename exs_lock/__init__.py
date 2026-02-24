"""
Session-Lock for Exs-Shell
"""

__version__ = "0.1.0"
__author__ = "kipoha"

import gi

from exs_lock.utils.screenshot import screenshot


gi.require_version("GtkSessionLock", "0.1")
gi.require_version("Gdk", "3.0")

from gi.repository import GtkSessionLock  # type: ignore  # noqa: E402

from fabric import Application  # noqa: E402

from exs_lock.lock.window import LockScreen  # noqa: E402
from exs_lock.utils.monitor import get_monitors, get_monitors_data  # noqa: E402


def initialize(app: Application):
    img_bytes = []
    for n in get_monitors_data():
        img_bytes.append(screenshot(n))
    for n, img in zip(get_monitors(), img_bytes):
        lock = GtkSessionLock.prepare_lock()
        lock.lock_lock()
        lockscreen = LockScreen(lock, app, img)
        lock.new_surface(lockscreen, n)
        lockscreen.show_all()


def main():
    app = Application("lock")
    initialize(app)
    app.run()


if __name__ == "__main__":
    main()

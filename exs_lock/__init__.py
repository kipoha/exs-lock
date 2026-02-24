"""
Session-Lock for Exs-Shell
"""

__version__ = "0.1.0"
__author__ = "kipoha"

import gi

gi.require_version("GtkSessionLock", "0.1")
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk, GtkSessionLock  # type: ignore  # noqa: E402

from fabric import Application  # noqa: E402

from exs_lock.lock.window import LockScreen  # noqa: E402


def initialize(app: Application):
    lock = GtkSessionLock.prepare_lock()
    lock.lock_lock()
    lockscreen = LockScreen(lock, app)
    lock.new_surface(lockscreen, Gdk.Display.get_default().get_monitor(0))
    lockscreen.show_all()


def main():
    app = Application("lock")
    initialize(app)
    app.run()


if __name__ == "__main__":
    main()

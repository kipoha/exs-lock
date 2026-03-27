import gi

gi.require_version("GtkSessionLock", "0.1")
gi.require_version("Gdk", "3.0")

from gi.repository import GtkSessionLock  # type: ignore  # noqa: E402

from fabric import Application  # noqa: E402

from exs_lock.modules.lock import LockScreen  # noqa: E402
from exs_lock.utils import css, monitor, screenshot  # noqa: E402


def initialize(app: Application):
    lock = GtkSessionLock.prepare_lock()
    lock.lock_lock()
    
    img_bytes = []
    for n in monitor.get_monitors_data():
        img_bytes.append(screenshot.take(n))
    
    screens = []
    
    for n, img in zip(monitor.get_monitors(), img_bytes):
        lockscreen = LockScreen(lock, app, img, screens)
        lock.new_surface(lockscreen, n)
        screens.append(lockscreen)
        lockscreen.show_all()


def lock():
    app = Application("exs-lock")
    file = css.load()
    app.set_stylesheet_from_file(file)
    initialize(app)
    app.run()


def lock_cmd(_):
    lock()

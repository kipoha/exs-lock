import pam
import getpass

from gi.repository import GtkSessionLock, GLib  # type: ignore

from fabric.widgets.window import Window
from fabric.widgets.image import Image
from fabric.widgets.entry import Entry
from fabric.widgets.box import Box
from fabric import Application


class LockScreen(Window):
    def __init__(self, lock: GtkSessionLock.Lock, app: Application):
        self.lock = lock
        self.app = app
        super().__init__(
            visible=False,
            anchor="top right",
            all_visible=False,
            child=Box(
                v_expand=False,
                children=[
                    Entry(
                        password=True,
                        on_activate=self.on_activate,
                    ),
                ],
            ),
        )

    def on_activate(self, entry: Entry, *args):
        if not pam.authenticate(getpass.getuser(), (entry.get_text() or "").strip()):
            return
        self.lock.unlock_and_destroy()
        self.destroy()
        GLib.idle_add(self.app.quit)

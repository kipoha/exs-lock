import pam
import getpass

from gi.repository import GtkSessionLock, GLib, GdkPixbuf, Gtk  # type: ignore

from fabric.widgets.window import Window
from fabric.widgets.overlay import Overlay
from fabric.widgets.entry import Entry
from fabric.widgets.box import Box
from fabric import Application


class LockScreen(Window):
    def __init__(
        self,
        lock: GtkSessionLock.Lock,
        app: Application,
        img_bytes: bytes,
    ):
        self.lock = lock
        self.app = app
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(img_bytes)
        loader.close()
        pixbuf = loader.get_pixbuf()
        image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        overlay = Overlay(
            image_widget,
            [
                Entry(
                    password=True,
                    on_activate=self.on_activate,
                ),
            ],
        )
        super().__init__(
            visible=False,
            anchor="top right",
            all_visible=False,
            child=Box(
                v_expand=False,
                children=[overlay],
            ),
        )

    def on_activate(self, entry: Entry, *args):
        if not pam.authenticate(getpass.getuser(), (entry.get_text() or "").strip()):
            return
        self.lock.unlock_and_destroy()
        self.destroy()
        GLib.idle_add(self.app.quit)

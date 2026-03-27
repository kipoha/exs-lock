import pam
import getpass

from typing import Any

from gi.repository import GtkSessionLock, GLib, GdkPixbuf  # type: ignore

from fabric import Application
from fabric.widgets.window import Window
from fabric.widgets.image import Image
from fabric.widgets.overlay import Overlay
from fabric.widgets.entry import Entry
from fabric.widgets.box import Box
from fabric.widgets.revealer import Revealer
from fabric.widgets.shapes import Corner, CornerOrientation

from exs_lock.utils.img import blur_png_bytes
from exs_lock.utils.config import get_config
from exs_lock.modules.widgets.clock import DateTime
from exs_lock.utils.loop import run_in_thread


class LockScreen(Window):
    def __init__(
        self,
        lock: GtkSessionLock.Lock,
        app: Application,
        img_bytes: bytes,
        all_screens: list["LockScreen"],
    ):
        self.lock = lock
        self.app = app
        self.all_screens = all_screens
        config = get_config()
        blurred = blur_png_bytes(img_bytes, config.blur_radius)
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(img_bytes)
        loader.close()
        pixbuf = loader.get_pixbuf()
        blurred_loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        blurred_loader.write(blurred)
        blurred_loader.close()
        blurred_pixbuf = blurred_loader.get_pixbuf()
        root_bg = Image(
            pixbuf=pixbuf,
            name="lockscreen-root-bg",
        )
        bg = Image(
            pixbuf=blurred_pixbuf,
            name="lockscreen-blurred-bg",
        )
        entry_position = {
            "top": "start",
            "center": "center",
            "bottom": "end",
        }
        self.entry = Entry(
            name="lockscreen-entry",
            placeholder="Password",
            password=not config.entry_visibility,
            on_activate=self.on_activate,
        )
        self.entry.connect("changed", self.on_change)
        self.box = Box(
            v_expand=True,
            h_expand=True,
            h_align="center",
            v_align="center",
            children=[self.entry],
            name="lockscreen-entry-box-inner",
            style_classes=config.entry_position,
        )
        if config.entry_position == "top":
            entry_childs = [
                Corner(
                    CornerOrientation.TOP_RIGHT,
                    style_classes="corner",
                    size=[50, 45],
                    v_align="start",
                ),
                self.box,
                Corner(
                    CornerOrientation.TOP_LEFT,
                    style_classes="corner",
                    size=[50, 45],
                    v_align="start",
                ),
            ]
        elif config.entry_position == "center":
            entry_childs = [self.box]
        else:  # bottom
            entry_childs = [
                Corner(
                    CornerOrientation.BOTTOM_RIGHT,
                    style_classes="corner",
                    size=[50, 45],
                    v_align="end",
                ),
                self.box,
                Corner(
                    CornerOrientation.BOTTOM_LEFT,
                    style_classes="corner",
                    size=[50, 45],
                    v_align="end",
                ),
            ]
        self.entry_box = Box(
            v_expand=False,
            h_expand=False,
            h_align="center",
            v_align=entry_position.get(config.entry_position, "end"),
            children=entry_childs,
            name="lockscreen-entry-box",
            style_classes=config.entry_position,
            all_visible=True,
        )
        widgets_box = Box(
            children=[
                DateTime(),
            ],
            h_expand=True,
            v_expand=True,
            h_align="center",
            v_align="center",
        )
        overlay = Overlay(
            widgets_box,
            [self.entry_box],
        )
        bg_overlay = Overlay(
            bg,
            [overlay],
        )
        self.revealer = Revealer(
            child=bg_overlay,
            name="lockscreen-revealer",
            transition_type="crossfade",
            transition_duration=500,
        )
        root_overlay = Overlay(
            root_bg,
            [self.revealer],
        )
        super().__init__(
            visible=False,
            anchor="lef top right bottom",
            all_visible=False,
            child=Box(
                v_expand=False,
                children=[root_overlay],
            ),
        )

    def show_all(self):
        _ = super().show_all()
        self.revealer.reveal()
        self.entry.grab_focus()
        return _

    def hide_and_destroy(self):
        for screen in self.all_screens:
            screen.revealer.unreveal()
        
        duration = getattr(self.revealer, "transition_duration", 500)

        def finish():
            self.lock.unlock_and_destroy()
            
            for screen in self.all_screens:
                super(LockScreen, screen).destroy()
                
            GLib.idle_add(self.app.quit)
            return False

        GLib.timeout_add(duration, finish)

    def on_change(self, entry: Entry, *_: Any):
        text = str(entry.get_text())
        if text:
            if "active" not in self.entry_box.style_classes:
                self.entry_box.add_style_class("active")
        else:
            if "active" in self.entry_box.style_classes:
                self.entry_box.remove_style_class("active")

    @run_in_thread
    def on_activate(self, entry: Entry, *_: Any):
        if not pam.authenticate(getpass.getuser(), (entry.get_text() or "").strip()):
            self.entry.add_style_class("error")
            GLib.timeout_add(1000, self.entry.remove_style_class, "error")
            return
        self.hide_and_destroy()

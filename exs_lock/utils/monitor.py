from gi.repository import Gdk, Gio  # type: ignore


class DisplayNotFoundError(Exception):
    """
    Raised when the display is not found (e.g., a Wayland compositor is not running).
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Display not found! Ensure you are running a Wayland compositor", *args
        )


class MonitorNotFoundError(Exception):
    """
    Raised when a monitor with the given ID is not found.

    Args:
        monitor_id: The ID of the monitor.
    """

    def __init__(self, monitor_id: int, *args: object) -> None:
        self._monitor_id = monitor_id
        super().__init__(f"No such monitor with id: {monitor_id}", *args)

    @property
    def monitor_id(self) -> int:
        """
        The ID of the monitor.
        """
        return self._monitor_id


def get_gdk_display() -> Gdk.Display:
    """
    Get the default :class:`Gdk.Display` or raise :class:`DisplayNotFoundError` if it's ``None``.

    Returns:
        The default :class:`Gdk.Display`.

    Raises:
        DisplayNotFoundError: If :func:`Gdk.Display.get_default` returned ``None``.
    """
    return Gdk.Display.get_default()


def get_monitor(monitor_id: int) -> "Gdk.Monitor | None":
    """
    Get the ``Gdk.Monitor`` by its ID.

    Args:
        monitor_id: The ID of the monitor.

    Returns:
        The monitor with the given ID, or ``None`` if no such monitor exists.
    """
    return get_gdk_display().get_monitor(monitor_id)


def get_n_monitors() -> int:
    """
    Get the number of monitors.

    Returns:
        The number of monitors.
    """
    return get_gdk_display().get_n_monitors()


def get_monitors() -> Gio.ListModel:
    """
    Get a list model of :class:`Gdk.Monitor`.

    Returns:
    A list model of :class:`Gdk.Monitor`.
    """
    monitors = [get_monitor(n) for n in range(get_n_monitors())]
    return monitors


def get_monitor_size(monitor_num: int) -> tuple[float, float]:
    monitor = get_monitor(monitor_num)
    geometry = monitor.get_geometry()  # type: ignore
    width, height = geometry.width, geometry.height
    return width, height


def get_monitor_data(monitor: int | Gdk.Monitor) -> tuple[int, int, int, int]:
    if isinstance(monitor, int):
        monitor = get_monitor(monitor)
    geometry = monitor.get_geometry()  # type: ignore
    return geometry.x, geometry.y, geometry.width, geometry.height


def get_monitors_data() -> list[tuple[int, int, int, int]]:
    monitors = []
    for m in get_monitors():
        geo = m.get_geometry()
        monitors.append((geo.x, geo.y, geo.width, geo.height))
    return monitors

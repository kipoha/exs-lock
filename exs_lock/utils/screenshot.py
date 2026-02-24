import subprocess


def screenshot(monitor_data: tuple[int, int, int, int]) -> bytes:
    x, y, width, height = monitor_data
    geometry = f"{x},{y} {width}x{height}"
    result = subprocess.run(
        ["grim", "-g", geometry, "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout

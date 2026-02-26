import sys

from exs_lock.utils.path import Dirs, Paths


def load() -> str:
    is_dev = "--dev" in sys.argv

    config_dir = Dirs.CONFIG_DIR / "lock"

    config_dir.mkdir(exist_ok=True)

    user_css = config_dir / "lock.css"
    user_colors = Dirs.CONFIG_DIR / "colors.css"
    user_imports = config_dir / "lock_imports.css"

    base_css = Paths.path / "styles/lock_base.css"
    base_colors = Paths.path / "styles/lock_colors.css"
    config_css = Paths.path / "styles/lock_custom.css"
    dev_css = Paths.path / "styles/lock.css"

    if is_dev:
        return str(dev_css)

    user_imports.touch()
    if not user_css.exists():
        user_css.touch()

        if not user_colors.exists():
            user_colors.touch()
            user_colors.write_text(base_colors.read_text())

        css_content = config_css.read_text()
        content = f"@import url('{user_imports}');\n\n{css_content}"
        user_css.write_text(content)
    user_imports.write_text(
        f'@import url("{user_colors}");\n@import url("{base_css}");'
    )

    return str(user_css)

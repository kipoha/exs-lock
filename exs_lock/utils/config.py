import json
from exs_lock.utils.path import Dirs
from exs_lock.interfaces.schemas import Config
from exs_lock.interfaces.types import AnyDict


initial_config = {
    "_lock": {
        "entry_visibility": False,
        "entry_position": "bottom",
        "blur_radius": 10,
    }
}


def get_config() -> Config:
    file = Dirs.CONFIG_DIR / "config.jsonc"
    if not file.exists():
        file.touch()
        file.write_text(json.dumps(initial_config, indent=2))
    data: AnyDict = json.loads(file.read_text())

    config: AnyDict = data.get("_lock", initial_config["_lock"])
    if not isinstance(config.get("entry_position"), str) or config[
        "entry_position"
    ] not in ["top", "center", "bottom"]:
        config["entry_position"] = "bottom"
    if (
        not isinstance(config.get("blur_radius"), (int, float))
        or config["blur_radius"] < 0
        or config["blur_radius"] > 100
    ):
        config["blur_radius"] = 10
    if not isinstance(config.get("entry_visibility"), bool):
        config["entry_visibility"] = False
    return Config(**config)

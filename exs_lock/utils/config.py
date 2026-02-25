import json
from exs_lock.utils.path import Dirs
from exs_lock.interfaces.schemas import Config
from exs_lock.interfaces.types import AnyDict


initial_config = {
    "_lock": {
        "entry_visibility": False,
        "entry_position": "bottom",
    }
}


def get_config() -> Config:
    file = Dirs.CONFIG_DIR / "config.jsonc"
    if not file.exists():
        file.touch()
        file.write_text(json.dumps(initial_config, indent=2))
    data: AnyDict = json.loads(file.read_text())

    config: AnyDict = data.get("_lock", initial_config["_lock"])
    return Config(**config)

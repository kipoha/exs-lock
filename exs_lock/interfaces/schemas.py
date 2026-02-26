from dataclasses import dataclass

from exs_lock.interfaces.types import EntryPosition


@dataclass
class Config:
    entry_visibility: bool = False
    entry_position: EntryPosition = "bottom"
    blur_radius: int = 10

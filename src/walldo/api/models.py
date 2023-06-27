from enum import StrEnum
from pydantic import BaseModel


class API(StrEnum):
    BASE = "https://wallies.cacko.net/api"
    ARTWORKS = "artworks"

class Wallpaper(BaseModel):
    title: str
    raw_src: str
    web_uri: str
    webp_src: str
    category: str
    colors: str
    id: str
    last_modified: float
    deleted: bool

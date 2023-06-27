from typing import Any, Optional
from .models import API, Wallpaper
import requests


class ClientMeta(type):

    __instance: Optional['Client'] = None

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwds)
        return cls.__instance
    
    def artworks(cls, page:int = 1) -> list[Wallpaper]:
        return cls().get_artworks(page)

class Client(object, metaclass=ClientMeta):

    def __call(self, path: API, **kwds):
        return requests.get(
            f"{API.BASE.value}/{path.value}",
            **kwds
        )

    def get_artworks(self, page: int = 1) -> list[Wallpaper]:
        res = self.__call(API.ARTWORKS, params=dict(page=page))
        data_json = res.json()
        return [Wallpaper(**x) for x in data_json]


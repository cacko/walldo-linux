from pathlib import Path
from walldo.wallpaper import set_lockscreen_wallpaper, setwallpaper
from walldo.api.client import Client
from random import randint, choice
from appdirs import user_data_dir
from walldo import __name__
from urllib.request import urlretrieve

USER_DATA = Path(user_data_dir(__name__))
WALLPAPERS_PATH =  USER_DATA / "wallpapers"
if not WALLPAPERS_PATH.exists():
    WALLPAPERS_PATH.mkdir(parents=True)
CURRENT_WALLPAPER = USER_DATA / "current"

def rotate():
    def get_images() -> list[Path]:
        results = list(WALLPAPERS_PATH.glob("*.png"))
        if len(results):
            return results
        for wps in Client.artworks(page=randint(1,10)):
            urlretrieve(
                wps.raw_src,
                (WALLPAPERS_PATH / f"{wps.id}.png").as_posix()
            )
        return list(WALLPAPERS_PATH.glob("*.png"))
        
    def get_image() -> Path:
        try:
            cwp_path = Path(CURRENT_WALLPAPER.read_text())
            cwp_path.unlink()
        except FileNotFoundError:
            pass
        images = get_images()
        return choice(images)

    image_path = get_image()
    set_lockscreen_wallpaper(filepath=image_path.as_posix())
    setwallpaper(filepath=image_path.as_posix())
    CURRENT_WALLPAPER.write_text(image_path.as_posix())

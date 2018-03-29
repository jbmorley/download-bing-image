import importlib

modules = ['osx', 'gnome']

setwallpaper_module = None
for module in modules:
    try:
        setwallpaper_module = importlib.import_module(f"setwallpaper.{module}")
        break
    except ImportError as e:
        print(e)
        continue

if setwallpaper_module is None:
    raise ImportError('Could not find any module to set wallpaper')

set_wallpaper = setwallpaper_module.set_wallpaper

#!/usr/bin/env python

modules = ['osx', 'gnome']

setwallpaper_module = None
for module in modules:
    try:
        setwallpaper_module = __import__(module, globals(), locals(), [], -1)
        break
    except ImportError:
        continue

if setwallpaper_module is None:
    raise ImportError('Could not find any module to set wallpaper')

set_wallpaper = setwallpaper_module.set_wallpaper

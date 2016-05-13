#!/usr/bin/env python

import os
import subprocess


GSETTINGS_PATH = "/usr/bin/gsettings"


if not os.path.exists(GSETTINGS_PATH):
    raise ImportError('gsetting does not exist on this system')


def set_wallpaper(wallpaper_path):
    subprocess.check_call([GSETTINGS_PATH, "set", "org.gnome.desktop.background", "picture-uri",
                          "file://%s" % (wallpaper_path)])

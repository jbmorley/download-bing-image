#!/usr/bin/env python3

import argparse
import json
import os
import platform
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request

import requests


def main():
    parser = argparse.ArgumentParser(description="Download the current bing.com image.")
    parser.add_argument("destination", help="Destination directory.")
    parser.add_argument("--set-desktop-picture",
                        action="store_true",
                        default=False,
                        dest="set",
                        help="set the macOS or Gnome desktop")
    parser.add_argument("--set", "-s",
                        action="store_true",
                        default=False,
                        dest="set",
                        help="set the macOS or Gnome desktop")
    parser.add_argument("--url",
                        default="https://www.bing.com",
                        help="URL to use (e.g., https://www.bing.com)")
    options = parser.parse_args()

    url = urllib.parse.urljoin(options.url, "HPImageArchive.aspx?format=js&n=1&idx=0")
    contents = requests.get(url).json()
    paths = [image["url"] for image in contents["images"]]

    images = []
    new_files = []

    destination_dir = os.path.abspath(options.destination)
    if not os.path.isdir(destination_dir):
        exit("Failed. '%s' is not a directory." % (destination_dir))

    for path in paths:
        url = "%s%s" % (options.url, path)

        # Deterime an appropriate filename; check to see if the destination URL matches an expected format and if so,
        # extract the identifier.
        _, filename = os.path.split(path)
        details = urllib.parse.urlparse(path)
        if details.path == "/th":
            filename = urllib.parse.parse_qs(details.query)['id'][0]

        destination = os.path.join(options.destination, filename)

        images.append(destination)

        if os.path.exists(destination):
            continue

        print(f"Downloading '{filename}'...")
        with tempfile.TemporaryDirectory() as p:
            temporary_path = os.path.join(p, filename)
            urllib.request.urlretrieve(url, temporary_path)
            shutil.move(temporary_path, destination)

        new_files.append(destination)

    if options.set and images:
        path = os.path.abspath(images[0])
        try:
            from setwallpaper import set_wallpaper
            set_wallpaper(path)
        except ImportError as e:
            exit("Unable to set desktop: %s" % e)

    print("Complete. %d new file(s)." % (len(new_files)))

if __name__ == "__main__":
    main()

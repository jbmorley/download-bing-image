#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request

import requests


class TempDir(object):

    def __init__(self):
        self.pwd = None
        self.path = None

    def __enter__(self):
        self.pwd = os.getcwd()
        self.path = tempfile.mkdtemp()
        os.chdir(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.pwd)
        shutil.rmtree(self.path)


def main():
    parser = argparse.ArgumentParser(description="Download the current bing.com image.")
    parser.add_argument("destination", help="Destination directory.")
    parser.add_argument("--set-desktop-picture",
                        action="store_true",
                        default=False,
                        help="set the OS X or Ubuntu desktop")
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
        with TempDir():
            urllib.request.urlretrieve(url, filename)
            shutil.move(filename, destination)

        new_files.append(destination)

    if options.set_desktop_picture and images:
        path = images[0]
        try:
            from setwallpaper import set_wallpaper
            set_wallpaper(path)
        except ImportError as e:
            exit("Unable to set desktop: %s" % e)

    print("Complete. %d new file(s)." % (len(new_files)))

if __name__ == "__main__":
    main()

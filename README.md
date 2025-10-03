> [!IMPORTANT]
> 
> This project has been archived and will not be maintained or developed further.

# download-bing-image

Download the current [bing.com](https://bing.com) image to a directory, optionally setting it as the OS X or Ubuntu desktop.

## Installation

```bash
git clone git@github.com:jbmorley/download-bing-image.git
cd download-bing-image
pipenv install
```

Usage
-----

```bash
download-bing-image --set-desktop-picture ~/Pictures
```

Cron
----

Since the bing.com image changes regularly, you may wish to schedule this to run using `cron`.

For example,

```cron
0 * * * * /path/to/download-bing-image --set-desktop-picture /Users/jbmorley/Pictures > /dev/null
```


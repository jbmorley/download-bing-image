download-bing-image
===================

Download the current [bing.com](https://bing.com) image to a directory, optionally setting it as the OS X or Ubuntu desktop.

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
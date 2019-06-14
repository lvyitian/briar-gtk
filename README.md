# Briar GTK

[![pipeline status](https://code.briarproject.org/NicoAlt/briar-gtk/badges/master/pipeline.svg)](https://code.briarproject.org/NicoAlt/briar-gtk/commits/master)
[![coverage report](https://code.briarproject.org/NicoAlt/briar-gtk/badges/master/coverage.svg)](https://code.briarproject.org/NicoAlt/briar-gtk/commits/master)

_Warning: This is still in a very early state and should be considered as prototype._

A simple GTK app for [Briar](https://briar.app), built with Python and GNOME Builder.
It uses the
[Briar REST API](https://code.briarproject.org/briar/briar/blob/master/briar-headless/README.md)
and therefore requires Java.

## Installation

So far, there is no official installation method and
you have to build it from source.

## Developers

The easiest and most convenient way is to build _briar-gtk_ using
[Builder](https://wiki.gnome.org/Apps/Builder).
In _Builder_, click "Clone Repository" at the bottom and
enter the URL to this Git project.

You can also call this:
```bash
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak-builder builddir --install-deps-from=flathub --user --install --force-clean --ccache app.briar.gtk.yaml
flatpak run app.briar.gtk
```

## Design Goals

* Intuitive UI, similar to Briar Android client
* Main platform is GNU/Linux, but should also support (at least) Windows and macOS
* Analogously, main platform is x86, but should also support (at least) arm
* Follows [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/stable/)
* Adaptive to different screen sizes (desktop and mobile devices)
* Has [phone constraints](https://developer.puri.sm/Librem5/Apps/Guides/Design/Constraints.html) in mind
* Strictly separates API wrapper from GTK stuff, making former a solid base for other (commandline) clients

## FAQ

### How can I add contacts?

Adding contacts isn't yet supported. Instead, you have to copy
the database and keys from a Briar Android installation. The most
convenient way to do so is by using
[_adb_](https://developer.android.com/studio/command-line/adb).
Note that your smartphone needs to be rooted for this.

1. Start _briar-gtk_ and register a dummy account. This will create
the needed directory structure at _~/.briar/_. Close the program afterwards.
2. Enable _adb_ on your smartphone and give it root permissions.
3. Connect via _adb_ and gain root permissions using `adb root`.
4. Copy all important files using `adb pull`:
_/data/data/org.briarproject.briar.android/app_db/db.mv.db_,
_/data/data/org.briarproject.briar.android/app_key/db.key_,
_/data/data/org.briarproject.briar.android/app_key/db.key.bak_
5. Replace the respecting files in _~/.briar/db_ and _~/.briar/key_.

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
[GNU Affero General Public License](LICENSE.md) for more details.

# Briar GTK

[![pipeline status](https://code.briarproject.org/NicoAlt/briar-gtk/badges/master/pipeline.svg)](https://code.briarproject.org/NicoAlt/briar-gtk/commits/master)
[![coverage report](https://code.briarproject.org/NicoAlt/briar-gtk/badges/master/coverage.svg)](https://code.briarproject.org/NicoAlt/briar-gtk/commits/master)

_Warning: This is still in a very early state and should be considered a prototype._

A simple GTK app for [Briar](https://briar.app), built with Python and GNOME Builder.
It uses [python-briar-wrapper](https://code.briarproject.org/briar/python-briar-wrapper) and the
[Briar REST API](https://code.briarproject.org/briar/briar/blob/master/briar-headless/README.md)
and therefore requires Java.

## Installation

So far, there is no official installation method and
you have to build it from source.

## Developers

The easiest and most convenient way is to build _briar-gtk_ using
[Builder](https://wiki.gnome.org/Apps/Builder).
Because Flatpak support is quite new in Builder,
it's recommend to install Builder via Flatpak:
```
flatpak install flathub org.gnome.Builder
```
To setup Flatpak on your system, check out the
[documentation at flatpak.org](https://flatpak.org/setup/).
In _Builder_, click "Clone Repository" at the bottom and
enter the URL to this Git project.

To build it on the command-line without Builder, call this:
```bash
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak-builder builddir --install-deps-from=flathub --user --install --force-clean --ccache app.briar.gtk.json
flatpak run app.briar.gtk
```

Additionally, you are able to run Briar GTK without Flatpak.
For this, you have to install Java, the
[Python dependencies](requirements.txt) and
[Briar headless](https://code.briarproject.org/briar/briar/blob/master/briar-headless/README.md).
Once you've done this, change the path of the Briar headless
jar in [briar_gtk.define](briar-gtk/briar_gtk/define.py),
build it with _meson_ and start Briar GTK.

Don't forget to initialize the briar-wrapper submodule:
`git submodule update --init`

### Internationalization

Feel free to add translations to Briar GTK by opening a merge request with
updates to the language file of your choice in _briar_gtk/po_. Make sure
to add your name to the _translator_credits_ list in
_briar-gtk/data/ui/about_dialog.ui.in_.

To test Briar GTK in your language, add the following entry to the
_finish-args_ list in _app.briar.gtk.json_:

```
--env=LC_ALL=de_DE.utf8
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

### How can I run this on the Librem 5?

Whether you own a Librem 5 or
[set up an emulator](https://developer.puri.sm/Librem5/Development_Environment/Boards/emulators.html),
you can install Briar GTK easily using Flatpak.

Before you start, you have to install some dependencies:

```bash
sudo apt install flatpak-builder elfutils
```

You can then simply
[follow the instructions from above](#developers).
Note that you currently don't get beyond the setup screen
because Briar Headless only works on x86 platforms so far.

---

For more questions, take a look at
[the FAQ of python-briar-wrapper](https://code.briarproject.org/briar/python-briar-wrapper/blob/master/README.md#faq).

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
[GNU Affero General Public License](LICENSE.md) for more details.

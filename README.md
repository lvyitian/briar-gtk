# Briar GTK

[![pipeline status](https://code.briarproject.org/briar/briar-gtk/badges/main/pipeline.svg)](https://code.briarproject.org/briar/briar-gtk/commits/main)
[![coverage report](https://code.briarproject.org/briar/briar-gtk/badges/main/coverage.svg)](https://code.briarproject.org/briar/briar-gtk/commits/main)

_Warning: This is still in a very early state and should be considered a prototype._

A simple GTK app for [Briar](https://briar.app), built with Python and GNOME Builder.
It uses [python-briar-wrapper](https://code.briarproject.org/briar/python-briar-wrapper) and the
[Briar REST API](https://code.briarproject.org/briar/briar/blob/master/briar-headless/README.md)
and therefore requires Java.

![Screenshot of Briar GTK showing conversation screen with two contacts and open chat with Alice](tools/screenshots/briar-gtk-screenshot-1.png)

For regular updates, check out the Briar tag on
[Nico Alt's blog](https://nico.dorfbrunnen.eu/tags/briar/)
([RSS feed](https://nico.dorfbrunnen.eu/tags/briar/index.xml)).

## Installation

### Flatpak

Alpha releases of Briar GTK can be installed using Flatpak.
After [installing Flatpak](https://flatpak.org/setup/), you can install
Briar GTK like this:
```
flatpak install --user https://flatpak.dorfbrunnen.eu/repo/appstream/app.briar.gtk.flatpakref
```

In case the above command doesn't work for you, you can try to install it manually:
```
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak remote-add --if-not-exists dorfbrunnen https://flatpak.dorfbrunnen.eu/repo/dorfbrunnen.flatpakrepo
flatpak install --user app.briar.gtk
```

#### Running

After installing Briar GTK, you can run it like this: 
```
flatpak run app.briar.gtk
```

## Developers

### GNOME Builder

The easiest and most convenient way to build _briar-gtk_ is by using
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

### flatpak-builder

To build it on the command-line without Builder, call this:
```bash
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak-builder --install-deps-from=flathub --user --install --force-clean --ccache flatpak-builddir app.briar.gtk.json
flatpak run app.briar.gtk
```

### Directly from source

After cloning this Git repository, don't forget to initialize the briar-wrapper submodule:
```
git submodule update --init
```

First, install some Debian dependencies:
```
sudo apt install meson libhandy-0.0-dev gettext appstream-util python3-pip
```

On Fedora, you can call:
```
sudo dnf install meson gtk3-devel libhandy-devel gettext libappstream-glib python3-pip
```

Then, install the Python dependencies:
```
pip3 install -r requirements.txt
```

You also need to build
[Briar Headless](https://code.briarproject.org/briar/briar/-/tree/master/briar-headless).
Check its readme to learn how to do it. You can also use
[builds provided by Nico Alt](https://media.dorfbrunnen.eu/briar/)
and put the .jar file at _~/.local/share/java/briar-headless.jar_.
Make sure to have _java_ (e.g. `openjdk-11-jdk`) installed.

Once you've done this, change the path to the Briar headless
jar in [briar_gtk.define](briar-gtk/briar_gtk/define.py) and
build Briar GTK with _meson_ and _ninja_:
```
meson --prefix $PWD/_install _build
ninja -C _build all install
```

You should then be able to run Briar GTK like this:
```
XDG_DATA_DIRS=_install/share:$XDG_DATA_DIRS ./_install/bin/briar-gtk
```

### Debian
First, install some Debian dependencies:
```
sudo apt install build-essential devscripts debhelper gnome-pkg-tools python3-all meson libhandy-0.0-dev gettext appstream-util
```

You can then build the .deb like this:
```
debuild -us -uc
```

And install the .deb like this:
```
sudo dpkg -i ../briar-gtk_0.1.0-alpha1-1_all.deb
```

## Internationalization

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
[the FAQ of python-briar-wrapper](https://code.briarproject.org/briar/python-briar-wrapper/blob/main/README.md#faq).

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
[GNU Affero General Public License](LICENSE.md) for more details.

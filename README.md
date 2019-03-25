# Briar GTK

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

## Design Goals

* Intuitive UI that follows the Briar Android client
* Main platform is GNU/Linux, but should also support Windows and macOS
* Follows [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/stable/)
* Adaptive to different screen sizes (desktop and mobile devices)
* Has [phone constraints](https://developer.puri.sm/Librem5/Apps/Guides/Design/Constraints.html) in mind
* Strictly separates API wrapper from GTK stuff, making former a solid base for other (commandline) clients

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
[GNU Affero General Public License](LICENSE.md) for more details.

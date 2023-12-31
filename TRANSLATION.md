Translation of Briar GTK is provided by the Localization Lab. To make
Briar GTK available in your language, please visit
https://www.transifex.com/otf/briar/ and ask to join one of the LocLab’s
language teams. You’ll then be able to contribute on
https://www.transifex.com/otf/briar/briar-gtk-pot/.

The Localization Lab has some instructions and advice for
translators at https://wiki.localizationlab.org/index.php/Briar.

#### Updating translations in Briar GTK

_This section is of interest only for developers of Briar GTK_.

To update translations locally, first install `transifex-client`. You can then pull updates with `tx pull -a`.
Afterwards, you should execute `tools/update-translations.sh` to let gettext finish the update.

The Localization Lab has some instructions and advice for
developers, too, at https://www.localizationlab.org/roles-guidelines#developer.

This is how updating translations in Briar GTK works:

* Transifex periodically fetches the source file from code.briarproject.org
* Translators submit their updates via Transifex
* We pull the updates from Transifex and commit them before each release
* Occasionally we make minor updates locally and push them to Transifex

Translations only happen on Transifex. You might want to make your changes through Transifex by joining the respective language teams.

To test Briar GTK in your language, add the following entry to the
_finish-args_ list in _app.briar.gtk.json_ when building Briar GTK with
flatpak-builder:

```
--env=LC_ALL=de_DE.utf8
```

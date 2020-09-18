Translations for this project are managed through Transifex:

https://transifex.com/otf/briar

If you'd like to volunteer as a translator, please create a Transifex account and request to be
added to the project's translation team. The Localization Lab has some instructions and advice for
translators here:

https://wiki.localizationlab.org/index.php/Briar

#### Updating translations in Briar GTK

_This section is of interest only for developers of Briar GTK_.

To update translations locally, first install `transifex-client`. You can then pull updates with `tx pull`.

This is how updating translations in Briar GTK works:

* Transifex periodically fetches the source file from code.briarproject.org
* Translators submit their updates via Transifex
* We pull the updates from Transifex and commit them before each release
* Occasionally we make minor updates locally and push them to Transifex

It's recommened not to edit translations locally in Git as Transifex uses a quite simple algorithm that doesn't support this use case. You might want to make your changes through Transifex instead, by joining the respective language teams.

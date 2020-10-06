#!/bin/bash
# Copyright (c) 2019-2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version from GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/generate_data.sh

cd briar-gtk/po
# git pull https://www.transifex.com/otf/briar/
>briar-gtk.pot
for file in ../data/app.briar.gtk.metainfo.xml.in ../data/ui/about_dialog.ui.in ../data/ui/*.ui $(find "../briar_gtk" -name '*.py');
do
xgettext --from-code=UTF-8 --no-location --no-wrap --keyword="_t:1c,2" -j $file -o briar-gtk.pot
done
>LINGUAS
for po in *.po
do
msgmerge --no-wrap -N $po briar-gtk.pot > /tmp/$$language_new.po
mv /tmp/$$language_new.po $po
language=${po%.po}
echo $language >>LINGUAS
done
sed -i -e '/^"POT-Creation-Date: /d' briar-gtk.pot
sed -i -e '/^"POT-Creation-Date: /d' *.po

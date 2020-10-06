#!/bin/bash
# Copyright (c) 2019-2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version from GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/generate_data.sh

function generate_translations()
{
    >$1
    for file in "${@:2}";
    do
        xgettext --from-code=UTF-8 --no-location --no-wrap -j $file -o $1
    done
    >LINGUAS
    for po in *.po
    do
        msgmerge --no-wrap -N $po $1 > /tmp/$$language_new.po
        mv /tmp/$$language_new.po $po
        language=${po%.po}
        echo $language >>LINGUAS
    done
    sed -i -e '/^"POT-Creation-Date: /d' $1
    sed -i -e '/^"POT-Creation-Date: /d' *.po
}

cd briar-gtk/po/briar-gtk
generate_translations "briar-gtk.pot" ../../data/ui/*.ui $(find "../../briar_gtk" -name '*.py') ../../data/ui/about_dialog.ui.in 

cd ../briar-gtk-meta
generate_translations "briar-gtk-meta.pot" ../../data/app.briar.gtk.metainfo.xml.in


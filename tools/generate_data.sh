#!/bin/bash
# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version from GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/generate_data.sh

function generate_resource()
{
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo '<gresources>'
    echo '  <gresource prefix="/app/briar/gtk">'
    for file in briar-gtk/data/ui/*.css
    do
        echo -n '    <file compressed="true">'
        echo -n $(basename $file)
        echo '</file>'
    done
    for file in briar-gtk/data/ui/*.ui about_dialog.ui
    do
        echo -n '    <file compressed="true" preprocess="xml-stripblanks">'
        echo -n $(basename $file)
        echo '</file>'
    done
    echo '  </gresource>'
    echo '</gresources>'
}

function generate_po()
{
    cd briar-gtk/po
    # git pull https://www.transifex.com/otf/briar/
    >briar-gtk.pot
    for file in ../data/app.briar.gtk.metainfo.xml.in ../data/ui/about_dialog.ui.in ../data/ui/*.ui $(find "../briar_gtk" -name '*.py');
    do
        xgettext --from-code=UTF-8 --no-location --no-wrap -j $file -o briar-gtk.pot
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
}

generate_resource > briar-gtk/data/ui/app.briar.gtk.gresource.xml
generate_po

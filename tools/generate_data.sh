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
    for file in data/ui/*.css
    do
        echo -n '    <file compressed="true">'
        echo -n 'ui/'
        echo -n $(basename $file)
        echo '</file>'
    done
    for file in data/ui/*.ui
    do
        echo -n '    <file compressed="true" preprocess="xml-stripblanks">'
        echo -n 'ui/'
        echo -n $(basename $file)
        echo '</file>'
    done
    echo '  </gresource>'
    echo '</gresources>'
}

function generate_po()
{
    cd po
    # git pull https://www.transifex.com/otf/briar/
    >briar-gtk.pot
    for file in ../data/app.briar.gtk.gschema.xml ../data/ui/*.ui $(find "../src/briar" -name '*.py');
    do
        xgettext --from-code=UTF-8 -j $file -o briar-gtk.pot
    done
    >LINGUAS
    for po in *.po
    do
        msgmerge -N $po briar-gtk.pot > /tmp/$$language_new.po
        mv /tmp/$$language_new.po $po
        language=${po%.po}
        echo $language >>LINGUAS
    done
}

generate_resource > data/ui/app.briar.gtk.gresource.xml
generate_po
#!/bin/bash
# Copyright (c) 2019-2020 Nico Alt
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
    for file in briar-gtk/data/ui/*.ui about_dialog.ui briar-gtk/data/ui/app.briar.gtk.gschema.xml
    do
        echo -n '    <file compressed="true" preprocess="xml-stripblanks">'
        echo -n $(basename $file)
        echo '</file>'
    done
    echo '  </gresource>'
    echo '</gresources>'
}

generate_resource > briar-gtk/data/ui/app.briar.gtk.gresource.xml

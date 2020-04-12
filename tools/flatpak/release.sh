#!/usr/bin/env bash
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

codedir=""
repodir=""
gpgfile=""

set -e -x

flatpak-builder --repo=$codedir/flatpak-repo --install-deps-from=flathub --user --force-clean --ccache $codedir/flatpak-builddir $codedir/app.briar.gtk.json
flatpak build-commit-from --src-repo=$codedir/flatpak-repo --gpg-sign=3D7EA4950100A0D222C970717C23232F3BF374D7 --update-appstream --no-update-summary $repodir
flatpak build-update-repo --default-branch=stable --gpg-import=$gpgfile --gpg-sign=3D7EA4950100A0D222C970717C23232F3BF374D7 --generate-static-deltas $repodir

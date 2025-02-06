#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Mobile auth - Alt Mobile domain input tool
#
# Copyright (C) 2024 Valentin Sokolov.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gettext import gettext as _
import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Adw, GLib, Gio

from mobileauth.window import Window


class Application(Adw.Application):

    version = "0.0.0"

    _window = None

    def __init__(self, application_id, version):
        super().__init__(
            application_id=application_id,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.version = version

        self.props.resource_base_path = "/io/github/SokolovValy/MobileAuth"
        GLib.set_application_name(_("Mobile Auth"))
        GLib.set_prgname(application_id)

        self._set_actions ()

    def _set_actions(self):
        action_entries = [
            ("quit", self._quit, ("app.quit", ["<Ctrl>Q"]))
        ]

        for action, callback, accel in action_entries:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect("activate", callback)
            self.add_action(simple_action)
            if accel is not None:
                self.set_accels_for_action(*accel)

    def _quit (self, action=None, param=None):
        self.quit()

    def do_activate(self):
        if not self._window:
            self._window = Window(self)
            self._window.set_default_icon_name(self.props.application_id)

        self._window.present()

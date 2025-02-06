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

from gi.repository import Gtk, Adw, GLib


@Gtk.Template(resource_path="/io/github/SokolovValy/MobileAuth/ui/welcome-dialog.ui")
class WelcomeDialog(Adw.Dialog):

    __gtype_name__ = "MobileAuthWelcomeDialog"

    status_page:Adw.StatusPage = Gtk.Template.Child()
    ok_button:Gtk.Button = Gtk.Template.Child()

    def __init__(self, domain_name):
        super().__init__(title=_("Admin Data"))

        self.status_page.props.title = _("Welcome to %s") % domain_name
        self.ok_button.connect("clicked", self.on_ok_button_clicked)
        
    def on_ok_button_clicked(self, button):
        self.close()

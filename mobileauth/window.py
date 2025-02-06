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

from gi.repository import Gtk, Adw, GLib, Gio, GObject

from mobileauth.admin_dialog import AdminDialog


@Gtk.Template(resource_path="/io/github/SokolovValy/MobileAuth/ui/window.ui")
class Window(Adw.ApplicationWindow):

    __gtype_name__ = "MobileAuthWindow"

    _app:Adw.Application = None

    toast_overlay:Adw.ToastOverlay = Gtk.Template.Child()
    domain_entry:Adw.EntryRow = Gtk.Template.Child()
    workgroup_entry:Adw.EntryRow = Gtk.Template.Child()
    host_name_entry:Adw.EntryRow = Gtk.Template.Child()
    submit_button:Gtk.Button = Gtk.Template.Child()
    clear_host_name_button:Gtk.Button = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__(application=app, title=_("Authentication"))

        self._app = app

        self.host_name_entry.connect("notify::text", self._on_entry_changed)
        self.host_name_entry.props.text = GLib.get_host_name()

        self.submit_button.connect("clicked", self._on_submit)

        self.clear_host_name_button.connect("clicked", self._on_clear_host_name)

        self._set_actions ()

    def _on_clear_host_name(self, button):
        self.clear_host_name()

    def clear_host_name(self):
        self.host_name_entry.props.text = GLib.get_host_name()

    def _on_entry_changed(self, object, prop):
        my_host_name = GLib.get_host_name()

        self.clear_host_name_button.props.visible = self.host_name_entry.props.text != my_host_name

    def _on_submit(self, button):
        domain = self.domain_entry.props.text
        workgroup = self.workgroup_entry.props.text
        host_name = self.host_name_entry.props.text

        if not domain or not workgroup or not host_name:
            self.toast_overlay.add_toast(Adw.Toast(title=_("Please fill in all fields.")))

            if not domain:
                self.domain_entry.add_css_class("error")
            if not workgroup:
                self.workgroup_entry.add_css_class("error")
            if not host_name:
                self.host_name_entry.add_css_class("error")

            return
        
        self.domain_entry.remove_css_class("error")
        self.workgroup_entry.remove_css_class("error")
        self.host_name_entry.remove_css_class("error")

        admin_dialog = AdminDialog(domain, workgroup, host_name)
        admin_dialog.present(self)

    def show_spinner(self):
        self.spinner_window = Gtk.Window(title=_("Please wait..."))
        self.spinner_window.set_default_size(200, 100)
        self.spinner_window.set_modal(True)

        spinner = Gtk.Spinner()
        spinner.set_size_request(50, 50)
        spinner.start()

        box = Gtk.Box(spacing=6)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.pack_start(spinner, True, True, 0)

        label = Gtk.Label(label=_("Operation in progress..."))
        box.pack_start(label, True, True, 0)

        self.spinner_window.add(box)
        self.spinner_window.show_all()

    def hide_spinner(self):
        if self.spinner_window:
            self.spinner_window.destroy()
            self.spinner_window = None

    def show_result_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self, flags=0, message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK, text=_("Result")
        )
        dialog.format_secondary_text(str(message))
        dialog.run()
        dialog.destroy()

    def _set_actions(self):
        action_entries = [
            ("about", self._show_about)
        ]

        for action, callback in action_entries:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect("activate", callback)
            self.add_action(simple_action)

    def _show_about(self, action=None, param=None):
        about = Adw.AboutDialog(
            application_icon=self._app.get_application_id(),
            application_name=_("Mobile Auth"),
            copyright="© 2024 Valentin Sokolov",
            designers=[
                "Vladimir Vaskov https://gitlab.gnome.org/Rirusha"
                ],
            developer_name="Valentin Sokolov",
            developers=[
                "Valentin Sokolov https://github.com/SokolovValy",
                "Vladimir Vaskov https://gitlab.gnome.org/Rirusha"
            ],
            license_type=Gtk.License.GPL_3_0,
            issue_url="https://github.com/SokolovValy/alt-mobile-auth/issues"
        )

        about.present(self)

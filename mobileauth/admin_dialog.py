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
import dbus
import threading

from gi.repository import Gtk, Adw, GLib

from mobileauth.welcome_dialog import WelcomeDialog


@Gtk.Template(resource_path="/io/github/SokolovValy/MobileAuth/ui/admin-dialog.ui")
class AdminDialog(Adw.Dialog):

    __gtype_name__ = "MobileAuthAdminDialog"

    main_stack:Gtk.Stack = Gtk.Template.Child()
    toast_overlay:Adw.ToastOverlay = Gtk.Template.Child()
    username_entry:Adw.EntryRow = Gtk.Template.Child()
    password_entry:Adw.PasswordEntryRow = Gtk.Template.Child()
    gpo_checkbutton:Gtk.CheckButton = Gtk.Template.Child()
    auth_button:Gtk.Button = Gtk.Template.Child()

    _domain = None
    _workgroup = None
    _host_name = None

    def __init__(self, domain, workgroup, host_name):
        super().__init__(title=_("Admin Data"))

        self._domain = domain
        self._workgroup = workgroup
        self._host_name = host_name

        self.auth_button.connect("clicked", self.on_auth)

    def on_auth(self, button):
        admin_username = self.username_entry.props.text
        admin_password = self.password_entry.props.text
        gpo_enabled = self.gpo_checkbutton.props.active

        command = f'write ad {self._domain} {self._host_name} {self._workgroup} "{admin_username}" "{admin_password}"'

        # Добавляем ключ --gpo, если включены групповые политики
        if gpo_enabled:
            command += " --gpo"

        threading.Thread(target=self.call_dbus_method, args=(command,)).start()

        self.start_loading()

    def call_dbus_method(self, command):
        try:
            bus = dbus.SystemBus()

            proxy = bus.get_object('org.altlinux.alterator', '/org/altlinux/alterator/mobile_auth')
            interface = dbus.Interface(proxy, dbus_interface='org.altlinux.alterator.authentication_mobile')

            response = interface.Join(command, timeout=120)

            stdout_output, stderr_output, return_code = response

            if return_code == 0:
                GLib.idle_add(self.success)
            elif return_code == 1:
                error_message = "\n".join(stderr_output) if stderr_output else _("Unknown error")
                GLib.idle_add(self.show_message, error_message)
            else:
                GLib.idle_add(self.show_message, _("An unknown error occurred"))

        except dbus.DBusException as e:
            GLib.idle_add(self.show_message, _("D-Bus Error: %s") % str(e))

        finally:
            GLib.idle_add(self.stop_loading)

    def success(self):
        self.force_close()
        dialog = WelcomeDialog(self._domain)
        dialog.present(self)

    def show_message(self, message):
        dialog = Adw.AlertDialog(
            heading=_("Error"),
            body=message
        )
        dialog.add_response("ok", _("Ok"))
        dialog.present(self)

    def start_loading(self):
        self.main_stack.props.visible_child_name = "loading"
        self.auth_button.props.visible = False
        self.props.can_close = False

    def stop_loading(self):
        self.main_stack.props.visible_child_name = "main"
        self.auth_button.props.visible = True
        self.props.can_close = True

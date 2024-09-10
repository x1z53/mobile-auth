#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import threading
import gi
import dbus
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class AdminDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Данные администратора", transient_for=parent, modal=True)

        self.set_default_size(250, 150)

        box = self.get_content_area()

        self.username_entry = Gtk.Entry()
        self.username_entry.set_text("administrator")
        self.username_entry.set_placeholder_text("Имя администратора")
        box.add(Gtk.Label(label="Имя администратора:"))
        box.add(self.username_entry)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)  
        self.password_entry.set_placeholder_text("Пароль")
        box.add(Gtk.Label(label="Пароль:"))
        box.add(self.password_entry)

        self.show_password_check = Gtk.CheckButton(label="Показать пароль")
        self.show_password_check.connect("toggled", self.on_show_password_toggled)
        box.add(self.show_password_check)

        self.gpo_check = Gtk.CheckButton(label="Включить групповые политики")
        box.add(self.gpo_check)

        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)

        self.show_all()

    def on_show_password_toggled(self, button):
        is_visible = button.get_active()
        self.password_entry.set_visibility(is_visible)

    def get_credentials(self):
        return self.username_entry.get_text(), self.password_entry.get_text(), self.gpo_check.get_active()

class SystemAuthApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Аутентификация")

        self.set_border_width(10)
        self.set_default_size(300, 150)

        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(grid)

        self.domain_entry = Gtk.Entry()
        grid.attach(Gtk.Label(label="Домен:"), 0, 0, 1, 1)
        grid.attach(self.domain_entry, 1, 0, 2, 1)

        self.workgroup_entry = Gtk.Entry()
        grid.attach(Gtk.Label(label="Рабочая группа:"), 0, 1, 1, 1)
        grid.attach(self.workgroup_entry, 1, 1, 2, 1)

        self.computer_name_entry = Gtk.Entry()
        grid.attach(Gtk.Label(label="Имя компьютера:"), 0, 2, 1, 1)
        grid.attach(self.computer_name_entry, 1, 2, 2, 1)

        self.submit_button = Gtk.Button(label="Продолжить")
        self.submit_button.connect("clicked", self.on_submit)
        grid.attach(self.submit_button, 0, 3, 3, 1)

        self.result_label = Gtk.Label()
        self.result_label.set_line_wrap(True)
        grid.attach(self.result_label, 0, 4, 3, 1)

    def on_submit(self, button):
        domain = self.domain_entry.get_text()
        workgroup = self.workgroup_entry.get_text()
        computer_name = self.computer_name_entry.get_text()

        if not domain or not workgroup or not computer_name:
            dialog = Gtk.MessageDialog(
                transient_for=self, flags=0, message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK, text="Ошибка",
            )
            dialog.format_secondary_text("Пожалуйста, заполните все поля.")
            dialog.run()
            dialog.destroy()
            return

        admin_dialog = AdminDialog(self)
        response = admin_dialog.run()

        if response == Gtk.ResponseType.OK:
            admin_username, admin_password, gpo_enabled = admin_dialog.get_credentials()
            command = f'write ad {domain} {computer_name} {workgroup} "{admin_username}" "{admin_password}"'

            if gpo_enabled:
                command += " --gpo"

            threading.Thread(target=self.call_dbus_method, args=(command,)).start()

        admin_dialog.destroy()

    def call_dbus_method(self, command):
        GLib.idle_add(self.show_spinner)

        try:
            bus = dbus.SystemBus()

            proxy = bus.get_object('ru.basealt.alterator', '/ru/basealt/alterator/mobile_auth')
            interface = dbus.Interface(proxy, dbus_interface='ru.basealt.alterator.authentication_mobile')

            response = interface.In_domain(command, timeout=120)

            stdout_output, stderr_output, return_code = response

            if return_code == 0:
                domain_name = self.domain_entry.get_text()
                result_str = f"Добро пожаловать в {domain_name}"
            elif return_code == 1:
                error_message = "\n".join(stderr_output) if stderr_output else "Неизвестная ошибка"
                result_str = f"Возникла следующая ошибка: {error_message}"
            else:
                result_str = "Произошла неизвестная ошибка"

            GLib.idle_add(self.show_result_dialog, result_str)

        except dbus.DBusException as e:
            GLib.idle_add(self.show_result_dialog, f"Ошибка D-Bus: {str(e)}")

        finally:
            GLib.idle_add(self.hide_spinner)


    def show_spinner(self):
        self.spinner_window = Gtk.Window(title="Подождите...")
        self.spinner_window.set_default_size(200, 100)
        self.spinner_window.set_modal(True)

        spinner = Gtk.Spinner()
        spinner.set_size_request(50, 50)
        spinner.start()

        box = Gtk.Box(spacing=6)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.pack_start(spinner, True, True, 0)

        label = Gtk.Label(label="Выполняется операция...")
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
            buttons=Gtk.ButtonsType.OK, text="Результат выполнения"
        )
        dialog.format_secondary_text(str(message))  
        dialog.run()
        dialog.destroy()

def main():
    app = SystemAuthApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()

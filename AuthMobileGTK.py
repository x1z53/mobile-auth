#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class AdminDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Данные администратора", transient_for=parent, modal=True)

        self.set_default_size(200, 100)

        # Основное содержимое окна
        box = self.get_content_area()

        # Поле для имени администратора
        self.username_entry = Gtk.Entry()
        self.username_entry.set_text("administrator")
        self.username_entry.set_placeholder_text("Имя администратора")
        box.add(Gtk.Label(label="Имя администратора:"))
        box.add(self.username_entry)

        # Поле для пароля
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)  # Скрытие пароля
        self.password_entry.set_placeholder_text("Пароль")
        box.add(Gtk.Label(label="Пароль:"))
        box.add(self.password_entry)

        # Чекбокс для показа/скрытия пароля
        self.show_password_check = Gtk.CheckButton(label="Показать пароль")
        self.show_password_check.connect("toggled", self.on_show_password_toggled)
        box.add(self.show_password_check)

        # Добавляем кнопки OK и Cancel
        self.add_button("OK", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)

        self.show_all()

    def on_show_password_toggled(self, button):
        # Переключение видимости пароля
        is_visible = button.get_active()
        self.password_entry.set_visibility(is_visible)

    def get_credentials(self):
        return self.username_entry.get_text(), self.password_entry.get_text()

class SystemAuthApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Настройки системы")

        self.set_border_width(10)
        self.set_default_size(400, 200)

        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(grid)

        # Поле ввода домена
        self.domain_entry = Gtk.Entry()
        grid.attach(Gtk.Label(label="Домен:"), 0, 0, 1, 1)
        grid.attach(self.domain_entry, 1, 0, 2, 1)

        # Поле ввода рабочей группы
        self.workgroup_entry = Gtk.Entry()
        grid.attach(Gtk.Label(label="Рабочая группа:"), 0, 1, 1, 1)
        grid.attach(self.workgroup_entry, 1, 1, 2, 1)

        # Поле ввода имени компьютера
        self.computer_name_entry = Gtk.Entry()
        grid.attach(Gtk.Label(label="Имя компьютера:"), 0, 2, 1, 1)
        grid.attach(self.computer_name_entry, 1, 2, 2, 1)

        # Кнопка для генерации команды
        self.submit_button = Gtk.Button(label="Сгенерировать команду")
        self.submit_button.connect("clicked", self.on_submit)
        grid.attach(self.submit_button, 0, 3, 3, 1)

        # Метка для отображения результата
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

        # Открытие диалогового окна для ввода данных администратора
        admin_dialog = AdminDialog(self)
        response = admin_dialog.run()

        if response == Gtk.ResponseType.OK:
            admin_username, admin_password = admin_dialog.get_credentials()
            command = f"system-auth write ad {domain} {computer_name} {workgroup} '{admin_username}' '{admin_password}'"
            self.result_label.set_text(f"Сгенерированная команда:\n{command}")
        admin_dialog.destroy()

def main():
    app = SystemAuthApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()

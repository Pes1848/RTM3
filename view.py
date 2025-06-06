"""Модуль представления (View) для отображения и управления ресурсами через GUI."""

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from model import Resource, load_resources_from_file, save_resources_to_file

logging.basicConfig(filename="errors.log", level=logging.ERROR, encoding="utf-8")


class ResourceApp(tk.Tk):
    """Главное окно приложения для управления ресурсами."""

    def __init__(self, resources):
        super().__init__()
        self.title("Учет ресурсов")
        self.geometry("700x400")

        self.resources = resources

        self.tree = ttk.Treeview(
            self, columns=("name", "date", "value", "frequency", "status"), show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.update_tree()

        form = tk.Frame(self)
        form.pack()

        self.name_entry = tk.Entry(form)
        self.name_entry.grid(row=0, column=0)
        self.date_entry = tk.Entry(form)
        self.date_entry.grid(row=0, column=1)
        self.value_entry = tk.Entry(form)
        self.value_entry.grid(row=0, column=2)
        self.freq_entry = tk.Entry(form)
        self.freq_entry.grid(row=0, column=3)
        self.status_var = tk.BooleanVar()
        self.status_check = tk.Checkbutton(form, text="Исправен", variable=self.status_var)
        self.status_check.grid(row=0, column=4)

        add_btn = tk.Button(form, text="Добавить", command=self.add_resource)
        add_btn.grid(row=1, column=0, columnspan=2)

        del_btn = tk.Button(form, text="Удалить", command=self.delete_selected)
        del_btn.grid(row=1, column=2, columnspan=2)

    def update_tree(self):
        """Обновляет таблицу ресурсов."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for res in self.resources:
            self.tree.insert("", tk.END, values=(res.name, res.date, res.value, res.frequency,
                                                 "исправен" if res.status else "неисправен"))

    def add_resource(self):
        """Добавляет ресурс в список и сохраняет."""
        try:
            new_res = Resource(
                self.name_entry.get(),
                self.date_entry.get(),
                float(self.value_entry.get()),
                self.freq_entry.get(),
                self.status_var.get()
            )
            self.resources.append(new_res)
            save_resources_to_file("test2.txt", self.resources)
            self.update_tree()
        except ValueError as ve:
            logging.error("Ошибка при добавлении ресурса: %s", ve)
            messagebox.showerror("Ошибка", str(ve))

    def delete_selected(self):
        """Удаляет выделенный ресурс."""
        selected = self.tree.selection()
        if not selected:
            return
        index = self.tree.index(selected[0])
        try:
            del self.resources[index]
            save_resources_to_file("test2.txt", self.resources)
            self.update_tree()
        except IndexError as ie:
            logging.error("Ошибка при удалении ресурса: %s", ie)


if __name__ == "__main__":
    try:
        RESOURCES = load_resources_from_file("test2.txt")
    except Exception as e:
        logging.error("Ошибка при загрузке файла: %s", e)
        RESOURCES = []
    app = ResourceApp(RESOURCES)
    app.mainloop()

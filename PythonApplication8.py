import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import re

class ResourceType:
    def __init__(self, name: str):
        self.name = name.strip('"')

    def __str__(self):
        return self.name


class ReadingDate:
    def __init__(self, date_str: str):
        self.date = datetime.strptime(date_str, "%Y.%m.%d")

    def __str__(self):
        return self.date.strftime("%Y.%m.%d")


class ReadingValue:
    def __init__(self, value: str):
        self.value = float(value)

    def __str__(self):
        return f"{self.value:.2f}"


class MeterReading:
    def __init__(self, resource: ResourceType, date: ReadingDate, value: ReadingValue, periodicity: str):
        self.resource = resource
        self.date = date
        self.value = value
        self.periodicity = periodicity.strip()

    def __str__(self):
        return f'"{self.resource.name}" {self.date.date.strftime("%Y.%m.%d")} {self.value.value} {self.periodicity}'


class FileManager:
    def __init__(self, filename: str):
        self.filename = filename

    def load_readings(self):
        readings = []
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file:
                tokens = re.findall(r'"[^"]*"|\d{4}\.\d{2}\.\d{2}|\d+\.\d+|\w+', line)
                if len(tokens) == 4:
                    reading = MeterReading(
                        ResourceType(tokens[0]),
                        ReadingDate(tokens[1]),
                        ReadingValue(tokens[2]),
                        tokens[3]
                    )
                    readings.append(reading)
        return readings

    def save_readings(self, readings):
        with open(self.filename, 'w', encoding='utf-8') as file:
            for reading in readings:
                file.write(str(reading) + '\n')


class AddReadingDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Ресурс:").grid(row=0)
        tk.Label(master, text="Дата (гггг.мм.дд):").grid(row=1)
        tk.Label(master, text="Значение:").grid(row=2)
        tk.Label(master, text="Периодичность:").grid(row=3)

        self.resource_entry = tk.Entry(master)
        self.date_entry = tk.Entry(master)
        self.value_entry = tk.Entry(master)
        self.periodicity_entry = tk.Entry(master)

        self.resource_entry.grid(row=0, column=1)
        self.date_entry.grid(row=1, column=1)
        self.value_entry.grid(row=2, column=1)
        self.periodicity_entry.grid(row=3, column=1)
        return self.resource_entry

    def apply(self):
        self.result = (
            self.resource_entry.get(),
            self.date_entry.get(),
            self.value_entry.get(),
            self.periodicity_entry.get()
        )


class MeterApp:
    def __init__(self, filename):
        self.file_manager = FileManager(filename)
        self.readings = self.file_manager.load_readings()

        self.root = tk.Tk()
        self.root.title("Учёт показаний")

        self.tree = ttk.Treeview(self.root, columns=("resource", "date", "value", "periodicity"), show="headings")
        self.tree.heading("resource", text="Ресурс")
        self.tree.heading("date", text="Дата")
        self.tree.heading("value", text="Значение")
        self.tree.heading("periodicity", text="Периодичность")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.populate_tree()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Добавить", command=self.add_reading).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_reading).pack(side=tk.LEFT, padx=5, pady=5)

    def populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in self.readings:
            self.tree.insert("", tk.END, values=(
                r.resource.name,
                r.date.date.strftime("%Y.%m.%d"),
                r.value.value,
                r.periodicity
            ))

    def add_reading(self):
        dialog = AddReadingDialog(self.root)
        if dialog.result:
            resource, date_str, value_str, periodicity = dialog.result
            try:
                reading = MeterReading(
                    ResourceType(resource),
                    ReadingDate(date_str),
                    ReadingValue(value_str),
                    periodicity
                )
                self.readings.append(reading)
                self.file_manager.save_readings(self.readings)
                self.populate_tree()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Неверные данные: {e}")

    def delete_reading(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            del self.readings[index]
            self.file_manager.save_readings(self.readings)
            self.populate_tree()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MeterApp("test2.txt")
    app.run()



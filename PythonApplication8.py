import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import List

FILE_NAME = "test2.txt"

class ResourceType:
    def __init__(self, value: str):
        self.value = value.strip('"')

    def __str__(self):
        return f'"{self.value}"'

class ReadingDate:
    def __init__(self, date_str: str):
        self.date = datetime.strptime(date_str, "%Y.%m.%d").date()

    def __str__(self):
        return self.date.strftime("%Y.%m.%d")

class ReadingValue:
    def __init__(self, value_str: str):
        self.value = float(value_str)

    def __str__(self):
        return f"{self.value}"

class MeterReading:
    def __init__(self, resource_type: ResourceType, date: ReadingDate, value: ReadingValue):
        self.resource_type = resource_type
        self.date = date
        self.value = value

    def __str__(self):
        return f"{self.resource_type} {self.date} {self.value}"

    def to_list(self):
        return [self.resource_type.value, str(self.date), str(self.value)]

def parse_line(line: str) -> MeterReading:
    import re
    tokens = re.findall(r'"[^"]*"|\d{4}\.\d{2}\.\d{2}|\d+\.\d+', line)
    return MeterReading(ResourceType(tokens[0]), ReadingDate(tokens[1]), ReadingValue(tokens[2]))

def read_all_readings() -> List[MeterReading]:
    readings = []
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    readings.append(parse_line(line.strip()))
    except FileNotFoundError:
        pass
    return readings

def write_all_readings(readings: List[MeterReading]):
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        for reading in readings:
            file.write(str(reading) + "\n")

class MeterReadingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Показания счетчиков")
        self.readings = read_all_readings()

        self.tree = ttk.Treeview(columns=("Тип ресурса", "Дата", "Значение"), show='headings')
        for col in ("Тип ресурса", "Дата", "Значение"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_type = tk.Entry()
        self.entry_date = tk.Entry()
        self.entry_value = tk.Entry()

        for i, (label_text, entry) in enumerate((
            ("Тип ресурса (в кавычках)", self.entry_type),
            ("Дата (гггг.мм.дд)", self.entry_date),
            ("Значение", self.entry_value))):
            tk.Label(root, text=label_text).pack()
            entry.pack()

        tk.Button(text="Добавить", command=self.add_reading).pack(pady=5)
        tk.Button(text="Удалить выбранное", command=self.delete_selected).pack(pady=5)

        self.update_tree()

    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for reading in self.readings:
            self.tree.insert('', tk.END, values=reading.to_list())

    def add_reading(self):
        try:
            new_reading = MeterReading(
                ResourceType(self.entry_type.get()),
                ReadingDate(self.entry_date.get()),
                ReadingValue(self.entry_value.get())
            )
            self.readings.append(new_reading)
            write_all_readings(self.readings)
            self.update_tree()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        for item in selected:
            values = self.tree.item(item)['values']
            self.readings = [r for r in self.readings if r.to_list() != list(map(str, values))]
        write_all_readings(self.readings)
        self.update_tree()

if __name__ == '__main__':
    root = tk.Tk()
    app = MeterReadingApp(root)
    root.mainloop()



"""Модуль содержит описание класса ресурса и функции загрузки/сохранения."""

import datetime
import logging

logging.basicConfig(filename="errors.log", level=logging.ERROR, encoding="utf-8")


class Resource:
    """Класс, представляющий ресурс с атрибутами: имя, дата, значение, периодичность, статус."""

    def __init__(self, name, date_str, value, frequency, status):
        self.name = name
        self.date = self._parse_date(date_str)
        self.value = float(value)
        self.frequency = self._validate_frequency(frequency)
        self.status = bool(status)

    def __str__(self):
        date_str = self.date.strftime("%Y.%m.%d")
        return f"{self.name} {date_str} {self.value} {self.frequency} {'исправен' if self.status else 'неисправен'}"

    @staticmethod
    def _parse_date(date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y.%m.%d").date()
        except ValueError as exc:
            raise ValueError("Дата должна быть в формате ГГГГ.ММ.ДД и быть корректной.") from exc

    @staticmethod
    def _validate_frequency(freq):
        valid = ["ежедневно", "еженедельно", "ежемесячно", "всегда"]
        if freq not in valid:
            raise ValueError(f"Недопустимая периодичность: {freq}")
        return freq


def load_resources_from_file(filename):
    """Загружает список ресурсов из текстового файла."""
    resources = []
    try:
        with open(filename, encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 5:
                    raise ValueError("Неверное количество элементов в строке.")
                name, date, value, freq, status_str = parts
                status = status_str.lower() in ("true", "исправен")
                resource = Resource(name, date, float(value), freq, status)
                resources.append(resource)
    except (ValueError, IndexError) as err:
        logging.error("Ошибка при чтении строки '%s': %s", line.strip(), err)
    except FileNotFoundError:
        logging.error("Файл '%s' не найден.", filename)
    return resources


def save_resources_to_file(filename, resources):
    """Сохраняет список ресурсов в текстовый файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for resource in resources:
                file.write(str(resource) + "\n")
    except IOError as err:
        logging.error("Ошибка при сохранении в файл: %s", err)





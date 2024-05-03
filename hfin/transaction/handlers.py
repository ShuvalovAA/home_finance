import csv
import os
from root.settings import TEMP_FILE_DIR
from typing import List, Optional

class Downloader():
    """Базовый класс для выгрузки файлов."""
    ENCODE = 'UTF-8'

    def __init__(self, separator: str, data: List[List], headers: Optional[List[str]]) -> None:
        self.separator = separator
        self.file_name = None
        self.data = data
        self.headers = headers

    def save_file(self):
        """Сохранить файл на носителе."""
        pass

    def get_file_name(self):
        """Получить путь до файла."""
        return self.file_name


class ExcelDownloader(Downloader):
    """Класс для выгрузки данных в формате excel."""

    pass


class CsvDownloader(Downloader):
    """Класс для выгрузки данных в формате csv."""

    def _set_headers(self, spamwriter):
        """Установить заголовки в файл."""
        if self.headers:
            spamwriter.writerow(self.headers)

    def save_file(self):
        file_name = 'test.csv'
        file_path = os.path.join(TEMP_FILE_DIR, file_name)
        with open(file_path, 'w', newline='') as csvfile:
            spamwriter = csv.writer(
                csvfile,
                delimiter=self.separator,
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL,
                )

            self._set_headers(spamwriter)
            for row in self.data:
                
                spamwriter.writerow(row)
        self.file_name = file_name


class FormatMapper():
    """Хранилище форматов файлов."""

    FILE_TYPE_MAP = {
        0: ExcelDownloader,
        1: CsvDownloader
    }

    SEPARATOR_MAP = {
        0: ';',
        1: ','
    }

    def get_downlader(self, file_type: int):
        """Получить класс выгрузки файла по формату."""
        return self.FILE_TYPE_MAP[file_type]

    def get_separator(self, separator_type: int):
        """Получить разделитель для файла."""
        return self.SEPARATOR_MAP[separator_type]


class DownloadDirector(FormatMapper):
    """Класс директор для загрузки файлов."""

    def __init__(self, separator_type: int, file_type: int, data: List[List], headers: Optional[List[str]]):
        self.separator = self.get_separator(separator_type)
        self.data = data
        self.headers = headers
        self.downloader = self.get_downlader(file_type)(
            separator=self.separator,
            data=self.data,
            headers=self.headers
        )

    def download(self):
        """Выгрузить данные файлом."""

        self.downloader.save_file()
        return self.downloader.get_file_name()

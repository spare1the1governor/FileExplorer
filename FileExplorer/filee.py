"""
Файл с основным функционалом программы
"""
import subprocess
import os
import time
from abc import ABC, abstractmethod
from validation import FileInputModel
from pydantic import ValidationError
from exceptions import FileNotFoundException,CurrentDirectoryError, FileNameFormatError


class FileManager:
    files = []

    def __init__(self):
        """определение местонахождения текущей директории"""
        try:
         self.current_path = os.getcwd()
        except Exception:
            raise CurrentDirectoryError


    def list_directory(self):
        """Вывод содержимого текущей папки."""
        print(f"Current directory: {self.current_path}")
        items = os.listdir(self.current_path)
        for item in items:
            # находим полный путь до файла
            full_path = os.path.join(self.current_path, item)
            if os.path.isfile(full_path):
                self.files.append(item)
                size = os.path.getsize(full_path) / (1024 ** 2)  # Размер в мегабайтах
                last_access = os.path.getatime(full_path)
                days_inactive = (time.time() - last_access) / (60 * 60 * 24)
                print(f"FILE {item} | Size: {size:.4f} MB | Days inactive: {int(days_inactive)}")
                if days_inactive > 100:
                    print(f" Would you like to delete the file '{item}'? It has been inactive for {int(days_inactive)} days.")
            elif os.path.isdir(full_path):
                for item in  items:
                    #находим п.п до папки
                    sizep = os.path.getsize(full_path) / (1024 ** 2)
                    time_of_creation = os.path.getctime(full_path)
                    print(f"DIR  {item} | Size: {sizep:.4f} MB | Time of creation : {time.ctime(time_of_creation) }")


    def move_back(self):
        """Перемещение в родительскую папку."""
        self.current_path = os.path.dirname(self.current_path)
        print(f"Moved back to: {self.current_path}")

    def create_file(self, filename):
        """Создание нового файла в текущей папке с проверкой имени файла."""
        try:
            # Валидация имени файла с помощью Pydantic
            valid_data = FileInputModel(filename=filename)
            full_path = os.path.join(self.current_path, valid_data.filename)
            # создание файла
            with open(full_path, 'w') as f:
                f.write(" ")  # Создаём пустой файл
            print(f"file {valid_data.filename} created ")
        except ValidationError() :
            # обработка ошибки  валидации
            raise FileNameFormatError()

    def open_file(self, name: str):
        """создание новго файла """
        if (name not in self.files):
            raise FileNotFoundException()
        os.startfile(name)

    @abstractmethod
    def get_user_input(self, prompt) -> str:
        """Абстрактный метод для ввода."""
        pass

    def run(self):
        """Основной цикл работы."""
        while True:
            self.list_directory()
            command = self.get_user_input('Enter command (create/move/delete/exit/open):')
            if command == 'create':
                filename = self.get_user_input('Enter file name: ')
                self.create_file(filename)
            elif command == 'move':
                self.move_back()
            elif command == 'open':
                name = self.get_user_input('what do you want to open?&')
                self.open_file(name)
            elif command == 'delete':
                filename = self.get_user_input('Enter file name to delete: ')
                full_path = os.path.join(self.current_path, filename)
                if os.path.exists(full_path):
                    os.remove(full_path)
                    print(f'File "{filename}" deleted.')
                else:
                    print('File not found.')
            elif command == "exit":
                print('Exiting the file manager.')
                break
            else:
                print('Invalid command. Try again.')


class ConsoleFileManager(FileManager):
    def get_user_input(self, prompt):
        return input(prompt)






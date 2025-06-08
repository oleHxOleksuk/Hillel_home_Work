from typing import List
import json
from book import Book
from book_model import BookModel

class LibraryFileManager:
    def __init__(self, file_name: str):
        self.__file_name = file_name  # Приватний атрибут для зберігання імені файлу
        self.__books = []  # Приватний атрибут для списку книг

    def __enter__(self):
        # Відкриваємо файл для читання або створюємо новий, якщо файл не існує
        try:
            with open(self.__file_name, 'r', encoding='utf-8') as file:
                self.__books = json.load(file)  # Завантажуємо список книг
        except (FileNotFoundError, json.JSONDecodeError):
            self.__books = []  # Якщо файл не знайдений або порожній, ініціалізуємо порожній список
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Завершуємо роботу з файлом, зберігаючи зміни
        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(self.__books, file, ensure_ascii=False, indent=4)

    # Приватний метод для збереження списку книг
    def __save_books(self, books: List[Book]):
        self.__books = [book.model.dict() for book in books]  # Перетворюємо книги в словники
        print("Книги збережено в файл.")

    # Приватний метод для завантаження списку книг
    def __load_books(self) -> List[Book]:
        return [Book(BookModel(**book)) for book in self.__books]  # Перетворюємо словники назад у книги

    # Публічний метод для збереження книг
    def save_books(self, books: List[Book]):
        self.__save_books(books)

    # Публічний метод для завантаження книг
    def load_books(self) -> List[Book]:
        return self.__load_books()

    # Аксесор для отримання списку книг (якщо потрібно)
    def get_books(self) -> List[Book]:
        return self.__load_books()
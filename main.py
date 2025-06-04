from pydantic import BaseModel
from typing import Optional, List, Generator
import json

# Декоратор для принту при додаванні книги
def log_add_book(func):
    def wrapper(self, book):
        print(f"Додається книга: {book.get_info()}")
        return func(self, book)
    return wrapper

# Декоратор для перевірки наявності книги в бібліотеці
def check_book_exists(func):
    def wrapper(self, book_title):
        # Перевірка, чи є книга з такою назвою
        book_found = any(book.model.book_title == book_title for book in self.books)
        if not book_found:
            print(f"Книга з назвою '{book_title}' не знайдена в бібліотеці.")
            return False
        return func(self, book_title)
    return wrapper

class BookModel(BaseModel):
    book_title: str
    author: str
    year_of_publication: str

class Book:
    def __init__(self, model: BookModel):
        self.model = model

    def get_info(self) -> str:
        return f"Назва: {self.model.book_title}, Автор: {self.model.author}, Рік видання: {self.model.year_of_publication}"

class Library:
    def __init__(self):
        self.books: List[Book] = []

    def list_books(self) -> List[str]:
        return [book.get_info() for book in self.books]

    #Додавання книги до бібліотеки
    @log_add_book
    def add_book(self,book:Book):
        self.books.append(book)

    # Видалення книги за назвою
    @check_book_exists
    def remove_book(self, book_title: str) -> bool:
        for book in self.books:
            if book.model.book_title == book_title:
                self.books.remove(book)
                return True
        return False

    # Ітератор для проходження по всіх книгах
    def __iter__(self):
        return iter(self.books)

    #Генератор для пошуку книг за автором
    def books_by_author(self, author: str) -> Generator[str, None, None]:
        for book in self.books:
            if book.model.author == author:
                yield book.get_info()

# Клас Контекстного Менеджера для роботи з файлами
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

if __name__ == '__main__':
    book_inst_1 = {
        'book_title': 'Fluent Python',
        'author': 'Luciano Ramalho',
        'year_of_publication': '2015'
    }
    book_inst_2 = {
        'book_title': "Кайдашева сім'я",
        'author': 'Іван Нечуй-Левицький',
        'year_of_publication': '1879'
    }
    #Створення моделей книг
    book_model_1 = BookModel(**book_inst_1)
    book_model_2 = BookModel(**book_inst_2)
    # Створення обєктів книг
    book_1 = Book(book_model_1)
    book_2 = Book(book_model_2)
    #Виведення інворміції про книги
    print(book_1.get_info())
    print(book_2.get_info())
    # Створення бібліотеки та додавання книг
    library = Library()
    library.add_book(book_1)
    library.add_book(book_2)
    # Використовуємо ітератор для проходження по всіх книгах
    print("Всі книги в бібліотеці:")
    for book in library:
        print(book.get_info())
    # Генератор для книг одного автора
    print('Пошук книги за втором: ')
    for book_info in library.books_by_author("Luciano Ramalho"):
        print(book_info)

    # Використання контекстного менеджера для збереження та завантаження книг
    file_name = 'library_books.json'

    # Додавання книг до списку
    library_books = [book_1, book_2]
    # Збереження списку книг в файл
    with LibraryFileManager(file_name) as file_manager:
        file_manager.save_books(library_books)

    # Завантаження списку книг з файлу
    with LibraryFileManager(file_name) as file_manager:
        loaded_books = file_manager.load_books()

    # Виведення завантажених книг
    print("\nЗавантажені книги з файлу:")
    for book in loaded_books:
        print(book.get_info())
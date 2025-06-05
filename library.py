from book import Book
from typing import List, Generator
from decorate import *

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
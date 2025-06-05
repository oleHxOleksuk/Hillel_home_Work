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
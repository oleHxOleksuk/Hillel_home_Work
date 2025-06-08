from book_model import BookModel
from book import Book
from journal import Journal
from library import Library
from library_file_manager import LibraryFileManager


if __name__ == '__main__':

    # Створення моделей книг
    book1_model = BookModel(book_title="Кайдашева сім'я", author="Іван Нечуй-Левицький", year_of_publication='1879')
    book2_model = BookModel(book_title="Зачарована Десна", author="Олександр Довженко", year_of_publication='1957')

    # Створення об'єктів книг
    book1 = Book(book1_model)
    book2 = Book(book2_model)

    # Створення журналу
    journal_model = BookModel(book_title="Мистецтво та культура", author="Артем Козак", year_of_publication='2023')
    journal = Journal(journal_model, issue_number=12)

    # Виведення інформації про книгу та журнал
    print(book1.get_info())  # Інформація про книгу
    print(book2.get_info())  # Інформація про книгу
    print(journal.get_info())  # Інформація про журнал

    # Створення бібліотеки та додавання книг
    library = Library()
    library.add_book(book1)
    library.add_book(book2)
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
    library_books = [book1, book2]
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

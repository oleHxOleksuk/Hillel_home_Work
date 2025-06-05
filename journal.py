from book import Book
from book_model import BookModel

class Journal(Book):
    def __init__(self, model: BookModel, issue_number: int):
        super().__init__(model)  # Викликаємо конструктор батьківського класу
        self.issue_number = issue_number  # Додатковий атрибут для журналу

    def get_info(self) -> str:
        # Додаємо номер випуску в інформацію про журнал
        return f"{super().get_info()}, Номер випуску: {self.issue_number}"

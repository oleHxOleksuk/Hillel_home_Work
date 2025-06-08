from book_model import BookModel

class Book:
    def __init__(self, model: BookModel):
        self.model = model

    def get_info(self) -> str:
        return f"Назва: {self.model.book_title}, Автор: {self.model.author}, Рік видання: {self.model.year_of_publication}"

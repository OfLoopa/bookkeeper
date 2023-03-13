from bookkeeper.bookkeeper_app import Bookkeeper
from bookkeeper.view.app import View
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


if __name__ == "__main__":
    app = Bookkeeper(
        view=View(), repository_factory=SQLiteRepository.repository_factory(
            models=[Category, Expense, Budget],
            db_file='bookkeeper/databases/client.sqlite.db'
        )
    )

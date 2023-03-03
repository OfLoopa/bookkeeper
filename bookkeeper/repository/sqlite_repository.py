"""
Модель реализует репозиторий, работающий с СУБД sqlite
"""
from inspect import get_annotations
import sqlite3
from typing import Any, Optional

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Класс репозитория, работающий с sqlite
    Методы:
        CRUD - add, get, update, delete, get_all
        Работа с таблицами - create_table, drop_table
        Адаптер для парсинга данных с СУБД - __parse_query_to_class
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls = cls
        self.create_table()

    def create_table(self) -> None:
        """
        Создает таблицу в базе данных, если она не существует
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            query = f"CREATE TABLE IF NOT EXISTS {self.table_name} (pk INTEGER PRIMARY KEY, "
            query += ', '.join(list(self.fields.keys())) + ')'
            cur.execute(query)
        con.close()

    def __parse_query_to_class(self, query: tuple[Any] | None) -> Optional[T] | None:
        if query is not None:
            out = self.cls(*query)
        else:
            out = None
        return out

    def drop_table(self) -> None:
        """
        Удаляет таблицу из базы данных
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"DROP TABLE {self.table_name}")
        con.close()

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        placeholders = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({placeholders})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            raw_res = cur.execute(
                f"SELECT * FROM {self.table_name} WHERE pk={pk}"
            )
            res = self.__parse_query_to_class(raw_res.fetchone())
        con.close()
        return res

    def get_all(self, where: dict[str, Any] | None = None) -> list[Optional[T]]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            raw_res = cur.execute(
                f"SELECT * FROM {self.table_name}"
            )
            res = raw_res.fetchall()
        con.close()
        out = [self.__parse_query_to_class(res[pk]) for pk in range(len(res))]
        return out

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            sql_query = f"UPDATE {self.table_name} SET "
            sql_query += ','.join([f"{attr} = {val}" for attr, val in obj.__dict__.items() if attr != 'pk'])
            sql_query += f" WHERE pk={obj.pk}"
            cur.execute(sql_query)
        con.close()

    def delete(self, pk: int) -> None:
        if pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f"DELETE FROM {self.table_name} WHERE pk={pk}"
            )
        con.close()

    @classmethod
    def repository_factory(cls, models: list[type], db_file: str) -> dict[type, type]:
        """
        Создает хэш с таблицами по моделям данных (Паттерн AbstractFactory)

        :param models: список классов, описывающих аннотацию типов в таблице
        :param db_file: относительный путь к СУБД
        :return: хэш с репозиториями для классов-аннотаций
        """
        return {model: cls(db_file, model) for model in models}

"""
Модель реализует репозиторий, работающий с СУБД sqlite
"""

from bookkeeper.repository.abstract_repository import AbstractRepository, T
from typing import Any
import sqlite3
from inspect import get_annotations
from dataclasses import dataclass


@dataclass
class Test:
    name: str
    pk: int = 0


class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls = cls
        self.__create_table()

    def __create_table(self):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
            if self.table_name in cur.fetchone():
                cur.execute(f"DROP TABLE {self.table_name}")
            query = "CREATE TABLE IF NOT EXISTS " + self.table_name + \
                    "(" + \
                    ', '.join([field for field in self.fields.keys()]) + ')'
            cur.execute(query)
        con.close()

    def __parse_query_to_class(self, query: tuple, pk: int):
        if query is not None:
            out = self.cls(*query)
            out.pk = pk
        else:
            out = None
        return out

    def drop(self) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"DROP TABLE {self.table_name}")
        con.close()

    def add(self, obj: T) -> int:
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
                f"SELECT * FROM {self.table_name} WHERE ROWID=={pk}"
            )
            res = self.__parse_query_to_class(raw_res.fetchone(), pk)
        con.close()
        return res

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            raw_res = cur.execute(
                f"SELECT * FROM {self.table_name}"
            )
            res = raw_res.fetchall()
        con.close()
        out = [self.__parse_query_to_class(res[pk], pk+1) for pk in range(len(res))]
        return out

    def update(self, obj: T) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            sql_query = f"UPDATE {self.table_name} SET " + \
                        ','.join([f"{attr} = {val}" for attr, val in obj.__dict__.items() if attr != 'pk']) + \
                        f" WHERE ROWID=={obj.pk}"
            cur.execute(sql_query)
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f"DELETE FROM {self.table_name} WHERE ROWID=={pk}"
            )
        con.close()

    @classmethod
    def repository_factory(cls, models: list, db_file: str):
        return {model: cls(db_file, model) for model in models}

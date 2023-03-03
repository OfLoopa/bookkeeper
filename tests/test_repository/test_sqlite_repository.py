from dataclasses import dataclass

from bookkeeper.repository.sqlite_repository import SQLiteRepository
import pytest


@pytest.fixture
def test_class():
    @dataclass
    class Custom:
        f: int = 1
        pk: int = 0
    return Custom


@pytest.fixture
def repos(test_class):
    return SQLiteRepository.repository_factory(models=[test_class], db_file='test.sqlite')


@pytest.fixture
def repo(repos, test_class):
    return repos[test_class]


def test_repo_factory(repos, test_class):
    obj = test_class()
    assert obj.pk == 0

    assert repos[test_class].db_file == 'test.sqlite' and repos[test_class].table_name == test_class.__name__.lower()


def test_crud(repo, test_class):
    obj = test_class(f=2)
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = test_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    obj3 = test_class(f=10, pk=2)
    repo.add(obj3)
    assert repo.get_all() == [obj2, obj3]
    repo.delete(pk)
    assert repo.get(pk) is None

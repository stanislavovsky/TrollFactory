from trollfactory.exceptions import InvalidStaticPropertyException
from trollfactory.datasets import *
from random import choices, choice
from typing import List, TypedDict
import unicodedata


def _ds(dataset, keyword, **kwargs):
    return getattr(globals()[dataset], keyword)


def _is_valid_first_name(person, **kwargs):
    name = person['name']['first_name']

    if type(name) != str or not len(name):
        return False

    # first character must be an uppercase letter
    if unicodedata.category(name[0]) != 'Lu':
        return False

    # rest of the characters must be lowercase letters
    for char in name[1:]:
        if unicodedata.category(char) != 'Ll':
            return False

    return True


def _generate_first_name(dataset, person, **kwargs):
    year = person['birthdate']['birth_year']
    names = _ds(dataset, 'MASCULINE_NAMES'
                if person['sex']['sex'] == 'male' else 'FEMININE_NAMES')

    if str(year) in names.keys():
        _year = str(year)
    elif year < int(sorted(names.keys())[0]):
        _year = sorted(names.keys())[0]
    else:
        _year = sorted(names.keys())[-1]


    return choices(population=names[_year]['names'],
                   weights=names[_year]['weights'])[0]


def _is_valid_surname(dataset, person, **kwargs):
    surname = person['name']['surname']

    # run the same checks as for first names #lesscode
    if not _is_valid_first_name({'name': {'first_name': surname}}):
        return False

    # check grammatical gender
    suffixes = _ds(dataset, 'SURNAME_SUFFIXES')
    for suffix in suffixes:
        if surname.endswith(suffix):
            if person['sex']['sex'] != suffixes[suffix][0]:
                return False
            break

    return True


def _generate_surname(dataset, person, **kwargs):
    surnames = _ds(dataset, 'MASCULINE_SURNAMES'
                   if person['sex']['sex'] == 'male' else 'FEMININE_SURNAMES')
    voivodeship = choice(list(surnames.keys()))  # TODO: use actual voivodeships

    return choices(population=surnames[voivodeship]['surnames'],
                   weights=surnames[voivodeship]['weights'])[0]


class NameType(TypedDict):
    first_name: str
    surname: str


class Name:
    DEPENDENCIES: List[str] = ['sex', 'birthdate']
    ORDER = ['first_name', 'surname']

    def __init__(self, person, dataset):
        self.person = {'name': {}, **person}
        self.data = {}
        self.dataset = dataset

    def generate(self) -> NameType:
        for _property in self.ORDER:
            if _property in self.person['name']:
                if globals()[f'_is_valid_{_property}'](
                    person=self.person, data=self.data, dataset=self.dataset):
                    self.data[_property] = self.person['name'][_property]
                else:
                    raise InvalidStaticPropertyException(
                        f'Invalid value for property "name.{_property}":'
                        f' {self.person["name"][_property]}.')
            else:
                self.data[_property] = globals()[f'_generate_{_property}'](
                    person=self.person, data=self.data, dataset=self.dataset)

        return self.data
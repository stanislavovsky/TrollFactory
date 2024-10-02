from trollfactory.exceptions import InvalidStaticPropertyException
from trollfactory.datasets import *
from random import randint, choices
from calendar import monthrange
from datetime import date
from typing import List, TypedDict


def _ds(dataset, keyword, **kwargs):
    return getattr(globals()[dataset], keyword)


def _is_valid_birth_year(person, **kwargs):
    now = date.today()
    year = person['birthdate']['birth_year']

    # the oldest person in modern history aged 122 years and 164 days
    if year not in range(now.year-123, now.year+1):
        return False

    if 'age' in person['birthdate']:
        age = person['birthdate']['age']

        if 'birth_month' in person['birthdate']:
            month = person['birthdate']['birth_month']

            if 'birth_day' in person['birthdate']:
                day = person['birthdate']['birth_day']

                if age != now.year-year-((now.month, now.day)<(month, day)):
                    return False

            elif age != now.year-year-(now.month<month):
                return False

        elif year not in (now.year-age, now.year-age-1):
            return False

    return True


def _generate_birth_year(dataset, person, **kwargs):
    now = date.today()

    if 'birthdate' in person and 'age' in person['birthdate']:
        age = person['birthdate']['age']

        if 'birth_month' in person['birthdate']:
            month = person['birthdate']['birth_month']

            if 'birth_day' in person['birthdate']:
                day = person['birthdate']['birth_day']
                return now.year-age-((now.month, now.day)<(month, day))
            else:
                return now.year-age-(now.month<month)
        else:
            return now.year-age

    age_groups = _ds(dataset, 'AGE_GROUPS')
    weights = (_ds(dataset, 'FEMALE_AGES_WEIGHTS')
               if person['sex']['sex'] == 'female'
               else _ds(dataset, 'MALE_AGES_WEIGHTS'))

    return now.year - randint(*choices(population=age_groups,
                                       weights=weights)[0])


def _is_valid_birth_month(person, data, **kwargs):
    now = date.today()
    month = person['birthdate']['birth_month']

    if data['birth_year'] == now.year and month > now.month:
        return False

    if month not in range(1, 13):
        return False

    return True


def _generate_birth_month(data, **kwargs):
    now = date.today()

    if data['birth_year'] == now.year:
        return randint(1, now.month)

    return randint(1, 12)


def _is_valid_birth_day(person, data, **kwargs):
    now = date.today()
    day = person['birthdate']['birth_day']
    
    if (data['birth_year'] == now.year
        and data['birth_month'] == now.month
        and day > now.day):
        return False
    
    if day not in range(1, monthrange(data['birth_year'],
                                      data['birth_month'])[1]+1):
        return False

    return True


def _generate_birth_day(data, **kwargs):
    now = date.today()

    if data['birth_year'] == now.year and data['birth_month'] == now.month:
        return randint(1, now.day)

    return randint(1, monthrange(data['birth_year'], data['birth_month'])[1])


def _is_valid_age(person, **kwargs):
    # the oldest person in modern history aged 122 years and 164 days
    return True if person['birthdate']['age'] in range(0, 123) else False


def _generate_age(data, **kwargs):
    today = date.today()
    return today.year - data['birth_year'] - (
        (today.month, today.day) < (data['birth_month'], data['birth_day']))


class BirthdateType(TypedDict):
    birth_year: int
    birth_month: int
    birth_day: int
    age: int


class Birthdate:
    DEPENDENCIES: List[str] = ['sex']
    ORDER = ['birth_year', 'birth_month', 'birth_day', 'age']

    def __init__(self, person, dataset):
        self.person = {'birthdate': {}, **person}
        self.dataset = dataset
        self.data = {}

    def generate(self) -> BirthdateType:
        for _property in self.ORDER:
            if _property in self.person['birthdate']:
                if globals()[f'_is_valid_{_property}'](person=self.person,
                                                       data=self.data):
                    self.data[_property] = self.person['birthdate'][_property]
                else:
                    raise InvalidStaticPropertyException(
                        f'Invalid value for property "birthdate.{_property}":'
                        f' {self.person["birthdate"][_property]}.')
            else:
                self.data[_property] = globals()[f'_generate_{_property}'](
                    person=self.person, data=self.data, dataset=self.dataset)

        return self.data
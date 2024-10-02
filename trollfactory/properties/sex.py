from trollfactory.exceptions import InvalidStaticPropertyException
from trollfactory.datasets import *
from random import choices
from typing import List, TypedDict


def _ds(dataset, keyword, **kwargs):
    return getattr(globals()[dataset], keyword)


def _is_valid_sex(person, **kwargs):
    return True if person['sex']['sex'] in ('female', 'male') else False


def _generate_sex(dataset, **kwargs):
    return choices(population=('female', 'male'),
                   weights=_ds(dataset, 'SEX_RATIO'))[0]


class SexType(TypedDict):
    sex: str


class Sex:
    DEPENDENCIES: List[str] = []
    ORDER = ['sex']

    def __init__(self, person, dataset):
        self.person = {'sex': {}, **person}
        self.data = {}
        self.dataset = dataset

    def generate(self) -> SexType:
        for _property in self.ORDER:
            if _property in self.person['sex']:
                if globals()[f'_is_valid_{_property}'](person=self.person,
                                                       data=self.data):
                    self.data[_property] = self.person['sex'][_property]
                else:
                    raise InvalidStaticPropertyException(
                        f'Invalid value for property "sex.{_property}":'
                        f' {self.person["sex"][_property]}.')
            else:
                self.data[_property] = globals()[f'_generate_{_property}'](
                    person=self.person, data=self.data, dataset=self.dataset)

        return self.data
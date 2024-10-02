from trollfactory.exceptions import InvalidStaticPropertyException
from trollfactory.datasets import *
from random import choices
from typing import List, TypedDict

BLOOD_TYPES = ('O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-')
BLOOD_TYPE_WEIGHTS = (35, 13, 30, 8, 8, 2, 2, 1)  # source: fuck knows


def _ds(dataset, keyword, **kwargs):
    return getattr(globals()[dataset], keyword)


def _is_valid_blood_type(person, **kwargs):
    if person['blood_type']['blood_type'] not in BLOOD_TYPES:
        return False
    return True


def _generate_blood_type(dataset, **kwargs):
    return choices(population=BLOOD_TYPES,
                   weights=BLOOD_TYPE_WEIGHTS)[0]


class BloodTypeType(TypedDict):
    blood_type: str


class BloodType:
    DEPENDENCIES: List[str] = []
    ORDER = ['blood_type']

    def __init__(self, person, dataset):
        self.person = {'blood_type': {}, **person}
        self.data = {}
        self.dataset = dataset

    def generate(self) -> BloodTypeType:
        for _property in self.ORDER:
            if _property in self.person['blood_type']:
                if globals()[f'_is_valid_{_property}'](person=self.person,
                                                       data=self.data):
                    self.data[_property] = self.person['blood_type'][_property]
                else:
                    raise InvalidStaticPropertyException(
                        f'Invalid value for property "blood_type.{_property}":'
                        f' {self.person["blood_type"][_property]}.')
            else:
                self.data[_property] = globals()[f'_generate_{_property}'](
                    person=self.person, data=self.data, dataset=self.dataset)

        return self.data
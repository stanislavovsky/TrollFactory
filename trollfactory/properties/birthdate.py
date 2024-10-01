from trollfactory.exceptions import InvalidStaticPropertyException
from random import randint

DATASETS = []
DEPENDENCIES = {}
ORDER = ['birth_month']


def _is_valid_birth_month(person, **kwargs):
    if person['birthdate']['birth_month'] in range(1, 13):
        return True
    return False


def _generate_birth_month(**kwargs):
    return randint(1, 12)


class Birthdate:
    def __init__(self, person):
        self.person = person
        self.data = {}

    def set_static_properties(self):
        if 'birthdate' in self.person:
            for _property in ORDER:
                if globals()[f'_is_valid_{_property}'](
                    person=self.person, data=self.data):
                    self.data[_property] = self.person['birthdate'][_property]
                else:
                    raise InvalidStaticPropertyException(
                        f'Invalid value for property "birthdate.{_property}":'
                        f' {self.person["birthdate"][_property]}.')

    def generate(self):
        self.set_static_properties()

        for _property in ORDER:
            if _property not in self.data:
                self.data[_property] = globals()[f'_generate_{_property}'](
                    person=self.person, data=self.data)

        return self.data
from trollfactory.exceptions import InvalidStaticPropertyException
from trollfactory.datasets import *
from random import choices


def _ds(dataset, keyword, **kwargs):
    return getattr(globals()[dataset], keyword)


def _is_valid_sex(person, **kwargs):
    return True if person['sex']['sex'] in ('female', 'male') else False


def _generate_sex(dataset, **kwargs):
    return choices(population=('female', 'male'),
                   weights=_ds(dataset, 'SEX_RATIO'))[0]


class Sex:
    DEPENDENCIES = []
    ORDER = ['sex']

    def __init__(self, person, dataset):
        self.person = person
        self.data = {}
        self.dataset = dataset

    def set_static_properties(self):
        if 'sex' in self.person:
            for _property in self.ORDER:
                if globals()[f'_is_valid_{_property}'](
                    person=self.person, data=self.data):
                    self.data[_property] = self.person['sex'][_property]
                else:
                    raise InvalidStaticPropertyException(
                        f'Invalid value for property "sex.{_property}":'
                        f' {self.person["sex"][_property]}.')

    def generate(self):
        self.set_static_properties()

        for _property in self.ORDER:
            if _property not in self.data:
                self.data[_property] = globals()[f'_generate_{_property}'](
                    person=self.person, data=self.data, dataset=self.dataset)

        return self.data
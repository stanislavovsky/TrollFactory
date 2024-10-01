from trollfactory.exceptions import InvalidStaticPropertyException
from random import choice

__datasets__ = []
__dependencies__ = {'sex': None}


def _is_valid_sex(sex):
    return True if sex in ('female', 'male') else False


class Sex:
    def __init__(self, properties):
        self.properties = properties

    def generate(self):
        data = {}

        if 'sex' in self.properties and 'sex' in self.properties['sex']:
            if _is_valid_sex(self.properties['sex']['sex']):
                data['sex'] = self.properties['sex']['sex']
            else:
                raise InvalidStaticPropertyException(
                    'Invalid value for property "sex.sex": '
                    f'{self.properties["sex"]["sex"]}.'
                    'Allowed values are: male, female.')
        else:
            data['sex'] = choice(('female', 'male'))

        return data
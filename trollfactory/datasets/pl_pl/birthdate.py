from json import loads
from pkgutil import get_data

_data = loads(get_data(__package__, 'assets/age_groups.json'))

AGE_GROUPS = _data['age_groups']
FEMALE_AGES_WEIGHTS = _data['female_weights']
MALE_AGES_WEIGHTS = _data['male_weights']
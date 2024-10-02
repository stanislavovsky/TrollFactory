from json import loads
from pkgutil import get_data

_names = loads(get_data(__package__, 'assets/names.json'))
SURNAMES = loads(get_data(__package__, 'assets/surnames.json'))
MASCULINE_NAMES = _names['masculine']
FEMININE_NAMES = _names['feminine']

SURNAME_SUFFIXES = {
    'ski': ('male', 'ska'),  # replace 'ski' with 'ska' in women's surnames
    'ska': ('female', 'ski'),
    'cki': ('male', 'cka'),
    'cka': ('female', 'cki'),
    'nny': ('male', 'nna'),
    'nna': ('female', 'nny'),
    'tny': ('male', 'tna'),
    'tna': ('female', 'tny'),
    'lny': ('male', 'lna'),
    'lna': ('female', 'lny'),
}
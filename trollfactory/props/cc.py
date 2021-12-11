"""Credit card data generation prop for TrollFactory."""

from typing import Optional, TypedDict
from random import randint, choice


CARD_TYPES: dict[str, tuple[tuple[str], int]] = {
    'americanexpress': (('34', '37'), 15),
    'diners': (('300', '301', '302', '303', '304', '305', '36', '38', '39'),
               14),
    'discover': (('6011', '622', '64', '65'), 16),
    'jcb': (('3088', '3096', '3112', '3158', '3337', '35'), 16),
    'mastercard': (('5', '2'), 16),
    'visa': (('4',), 16),
}


class CcDataType(TypedDict):
    """Type hint for the credit card data."""

    number: int
    cvv3: int
    cvv4: int
    expiry_date: str
    service_code: int
    pvv: int
    track1: str
    track2: str


class CcType(TypedDict):
    """Type hint for the credit card data property."""

    prop_title: str
    americanexpress: CcDataType
    diners: CcDataType
    discover: CcDataType
    jcb: CcDataType
    mastercard: CcDataType
    visa: CcDataType


def generate_card_number(card_type: str) -> int:
    """Generate a CC number."""
    number = choice(CARD_TYPES[card_type][0])
    number += ''.join([str(randint(1, 9)) for _ in range(
        CARD_TYPES[card_type][1] - len(number) - 1)])

    digits = list(map(int, number + '0'))
    luhn = (
        sum(digits[-1::-2])
        + sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    ) % 10

    return int(number + str((10 - luhn) % 10))


def generate_cvv3() -> int:
    """Generate a 3-digit CVV number."""
    return randint(100, 999)


def generate_cvv4() -> int:
    """Generate a 4-digit CVV number."""
    return randint(1000, 9999)


def generate_expiry_date() -> str:
    """Generate a CC expiry date."""
    return str(randint(1, 12)).zfill(2) + '/' + str(randint(25, 33))


def generate_service_code() -> int:
    """Generate CC service code."""
    # 221 is the typical value, it means international interchange,
    # IC, contact issuer via online means, no restrictions
    return 221


def generate_pvv() -> int:
    """Generate Pin Verification Value."""
    return randint(1000, 9999)


def generate_track1(card_type, card_number, card_name, card_expiry_date,
                    service_code, card_cvv) -> str:
    """Generate track 1 string of the magnetic stripe."""
    return ('B' + str(card_number) + '^' + card_name + '^'
            + card_expiry_date.replace('/', '') + str(service_code))


def generate_track2(card_type, card_number, card_expiry_date, service_code,
                    pvv, card_cvv) -> str:
    """Generate track 2 string of the magnetic stripe."""
    track2: str = ''

    if card_type == 'mastercard':
        track2 += ';'

    track2 += (str(card_number) + '=' + card_expiry_date.replace('/', '')
               + str(service_code))

    if card_type == 'mastercard':
        track2 += '000000000'  # discretionary data
    else:
        track2 += str(pvv)

    track2 += str(card_cvv)
    track2 += '?' if card_type == 'mastercard' else '0'

    return track2


class Cc:
    """Credit card data generation prop for TrollFactory."""

    def __init__(self, properties: dict) -> None:
        self.properties = properties
        self.unresolved_dependencies: list[str] = []

        for dependency in ('name', 'birthdate'):
            if dependency not in self.properties:
                self.unresolved_dependencies.append(dependency)

    def generate(self) -> Optional[CcType]:
        """Generate the credit card data."""
        # Used properties
        age: int = self.properties['birthdate']['age']
        name: str = self.properties['name']['name']
        surname: str = self.properties['name']['surname']

        if age < 18:
            return None

        data: CcType = {
            'prop_title': 'CC',
        }

        for card_type in CARD_TYPES:
            data[card_type]: CcDataType = {
                'number': generate_card_number(card_type),
                'cvv3': generate_cvv3(),
                'cvv4': generate_cvv4(),
                'expiry_date': generate_expiry_date(),
                'service_code': generate_service_code(),
                'pvv': generate_pvv(),
            }

            data[card_type]['track1']: str = generate_track1(
                    card_type, data[card_type]['number'],
                    '/'.join([name, surname]), data[card_type]['expiry_date'],
                    data[card_type]['service_code'], data[card_type]['cvv3'])
            data[card_type]['track2']: str = generate_track2(
                    card_type, data[card_type]['number'],
                    data[card_type]['expiry_date'],
                    data[card_type]['service_code'],
                    data[card_type]['pvv'], data[card_type]['cvv3'])

        return data

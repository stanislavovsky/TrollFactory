"""Measurements generation prop for TrollFactory."""

from random import randint

AVERAGES = {0: (5, 10, 50, 90), 1: (5, 10, 50, 90), 2: (10, 16, 80, 95),
            3: (12, 20, 89, 102), 4: (13, 22, 90, 113), 5: (15, 25, 102, 120),
            6: (16, 29, 107, 129), 7: (18, 34, 113, 135),
            8: (20, 41, 119, 141), 9: (22, 48, 124, 147),
            10: (25, 53, 128, 154), 11: (27, 59, 134, 160),
            12: (30, 67, 139, 167), 13: (33, 75, 140, 176),
            14: (37, 78, 150, 182), 15: (42, 80, 152, 186),
            16: (44, 82, 153, 189), 17: (45, 87, 154, 190),
            18: (47, 88, 155, 190), 19: (50, 120, 156, 205)}


class Measurements:
    """Measurements generation prop class."""

    def __init__(self, properties: dict) -> None:
        """Measurements generation prop init function."""
        self.properties = properties
        self.unresolved_dependencies = ['birthdate'] if 'birthdate' not in \
            properties else []

    def generate(self) -> dict:
        """Generate the measurements."""
        age = self.properties['birthdate']['age']

        if age in range(0, 20):
            weight = randint(AVERAGES[age][0], AVERAGES[age][1])
            height = randint(AVERAGES[age][2], AVERAGES[age][3])
        else:
            weight = randint(50, 120)
            height = randint(156, 205)

        return {
            'prop_title': 'Measurements',
            'weight': weight,
            'height': height,
            'bmi': "{:.2f}".format(weight / ((height / 100) * (height / 100))),
        }

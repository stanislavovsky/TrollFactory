#!/usr/bin/env python3
from trollfactory import datasets, properties
from trollfactory.properties import *
from trollfactory.exceptions import InvalidDatasetException

AVAILABLE_DATASETS = ['_'.join([i[0], i[1].upper()])
                      for i in [i.split('-') for i in datasets.__all__]]


def _is_valid_dataset(dataset):
    return True if dataset in AVAILABLE_DATASETS else False


def generate_person(dataset,
                    static_properties={},
                    exclude_properties=[]):
    if not _is_valid_dataset(dataset):
        raise InvalidDatasetException(f'Invalid dataset: {dataset}. '
            f'Available datasets are: {AVAILABLE_DATASETS}.')

    person = {**static_properties}
    dataset = dataset.replace('_', '-').lower()
    used_properties = [i for i in properties.__all__
                       if i not in exclude_properties]

    for _property in used_properties:
        Property = getattr(globals()[_property], ''.join(
            [i.capitalize() for i in _property.split('_')]))
        person[_property] = Property(person, dataset).generate()

    return person
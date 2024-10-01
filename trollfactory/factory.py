#!/usr/bin/env python3
from trollfactory import datasets, properties
from trollfactory.properties import *
from trollfactory.exceptions import InvalidDatasetException
from sys import modules

AVAILABLE_DATASETS = ['_'.join([i[0], i[1].upper()])
                      for i in [i.split('-') for i in datasets.__all__]]


def _is_valid_dataset(dataset):
    return True if dataset in AVAILABLE_DATASETS else False


def generate_person(dataset,
                    static_properties={},  # TODO
                    exclude_properties=None,  # TODO
                    only_properties=[]):  # TODO
    if not _is_valid_dataset(dataset):
        raise InvalidDatasetException(f'Invalid dataset: {dataset}. '
            f'Available datasets are: {AVAILABLE_DATASETS}.')

    person = {}

    for _property in properties.__all__:
        Property = getattr(modules[f'trollfactory.properties.{_property}'],
                           _property.capitalize())
        person[_property] = Property(person).generate()

    return person
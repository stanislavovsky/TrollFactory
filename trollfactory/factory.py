#!/usr/bin/env python3
from trollfactory import datasets, properties
from trollfactory.properties import *
from trollfactory.exceptions import InvalidDatasetException, \
                                    UnresolvedDependencyException

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
    properties_list = [i for i in properties.__all__
                       if i not in exclude_properties]
    remaining = properties_list.copy()

    while len(remaining) > 0:
        for _property in remaining:
            Property = getattr(globals()[_property], ''.join(
                [i.capitalize() for i in _property.split('_')]))
            dependencies_met = True

            for dependency in Property.DEPENDENCIES:
                if dependency not in properties_list:
                        raise UnresolvedDependencyException(
                            f'Dependency {dependency} could not be resolved.')
                if dependency not in person:
                    dependencies_met = False
                    break
            
            if dependencies_met:
                person[_property] = Property(person, dataset).generate()
                remaining.remove(_property)

    return person
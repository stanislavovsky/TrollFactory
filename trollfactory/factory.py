#!/usr/bin/env python3
from trollfactory import datasets, properties
from trollfactory.properties import *
from trollfactory.datasets import *
from trollfactory.exceptions import InvalidDatasetException, \
                                    UnresolvedDependencyException

AVAILABLE_DATASETS = ['_'.join([i[0], i[1].upper()])
                      for i in [i.split('_') for i in datasets.__all__]]


def _is_valid_dataset(dataset):
    return True if dataset in AVAILABLE_DATASETS else False


def _get_property_class(_property):
    return getattr(globals()[_property],
                   ''.join([i.capitalize() for i in _property.split('_')]))


def _lp(dataset, _property):
    strings = getattr(globals()[dataset], 'PROPERTIES')

    if _property in strings:
        return strings[_property]
    return _property.split('.')[-1]


def _lv(dataset, key, value):
    if type(value) != str:
        return value

    strings = getattr(globals()[dataset], 'VALUES')

    if key in strings and value in strings[key]:
        return strings[key][value]
    return value


def list_available_datasets():
    return [{
        'dataset': f'{dataset.split("_")[0]}_{dataset.split("_")[1].upper()}',
        'module_name': dataset,
        'language': getattr(globals()[dataset], 'LANGUAGE'),
        'country_full': getattr(globals()[dataset], 'COUNTRY_FULL'),
        'country_shorthand': getattr(globals()[dataset], 'COUNTRY_SHORTHAND'),
        'emoji': getattr(globals()[dataset], 'EMOJI'),
    } for dataset in datasets.__all__]


class Person():
    def __init__(self,
                 dataset,
                 static_properties={},
                 exclude_properties=[]):
        if not _is_valid_dataset(dataset):
            raise InvalidDatasetException(f'Invalid dataset: {dataset}. '
                f'Available datasets are: {AVAILABLE_DATASETS}.')

        self.person = {**static_properties}
        self.dataset = dataset.lower()
        self.properties_list = [i for i in properties.__all__
                                if i not in exclude_properties]

    def localized(self):
        return {_lp(self.dataset, _property): {
            _lp(self.dataset, f'{_property}.{i}'): \
            _lv(self.dataset, f'{_property}.{i}', self.person[_property][i])
            for i in self.person[_property]
        } for _property in self.person}

    def generate(self):
        remaining = self.properties_list[:]

        while len(remaining) > 0:
            for _property in remaining:
                Property = _get_property_class(_property)
                dependencies_met = True

                for dependency in Property.DEPENDENCIES:
                    if dependency not in self.properties_list:
                            raise UnresolvedDependencyException(
                                f'Dependency {dependency} could not be resolved.')
                    if dependency not in self.person:
                        dependencies_met = False
                        break
                
                if dependencies_met:
                    self.person[_property] = Property(self.person,
                                                      self.dataset).generate()
                    remaining.remove(_property)
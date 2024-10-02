class InvalidStaticPropertyException(Exception):
    '''An exception raised when the value of a static property is incorrect.'''


class InvalidDatasetException(Exception):
    '''An exception raised when the selected dataset is incorrect or unavailable.'''


class UnresolvedDependencyException(Exception):
    '''An exception raised when the property dependencies cannot be resolved.'''
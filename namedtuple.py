import traceback
import sys


def make_namedtuple(typename, *fields, **fields_with_default):
    """
    helper to create a named tuple with some default values
    :param typename: name of the type
    :param fields: required argument of the named tuple
    :param fields_with_default: positional arguments with fields and their default value
    :return: the namedtuple

    >>> Bob = namedtuple('Bob', 'a', 'b', c=2, d=14)
    >>> Bob(a=12, b=14)
    Bob(a=12, b=14, d=14, c=2)
    >>> Bob(a=12, d=123)
    Bob(a=12, b=14, d=123, c=2)
    >>> Bob(a=12)
    Traceback (most recent call last):
    TypeError: __new__() missing 1 required positional argument: 'b'
    >>> Bob()
    Traceback (most recent call last):
    TypeError: __new__() missing 2 required positional arguments: 'a' and 'b'
    """

    import collections
    field_names = list(fields) + list(fields_with_default.keys())
    T = collections.namedtuple(typename, field_names)
    T.__new__.__defaults__ = tuple(fields_with_default.values())
    return T

Bob = make_namedtuple('Bob', 'a', 'b', c=2, d=14)

print('debut')
print(Bob)

print('bob ?')
print(Bob(a=12, b=14))

print('booooooob')
print(Bob(a=12, b=14, c=123))

print('boooooooum')
try:
    print(Bob())
except:
    traceback.print_exc(file=sys.stdout)

print('boooooooum2')
try:
    print(Bob(a=12))
except:
    traceback.print_exc(file=sys.stdout)

print('boooooooum3')
try:
    print(Bob(b=12))
except:
    traceback.print_exc(file=sys.stdout)
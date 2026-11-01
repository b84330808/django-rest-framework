"""
Wrapper for the builtin json module that ensures compliance with the JSON spec.

REST framework should always import this wrapper module in order to maintain
spec-compliant encoding/decoding. Support for non-standard features should be
handled by users at the renderer and parser layer.
"""
import functools
import json  # noqa
import math


def strict_constant(o):
    raise ValueError('Out of range float values are not JSON compliant: ' + repr(o))


def strict_float(o):
    # Literals such as `1e999` don't reach `parse_constant`, but still
    # overflow to infinity when converted to a float.
    value = float(o)
    if math.isinf(value):
        strict_constant(o)
    return value


@functools.wraps(json.dump)
def dump(*args, **kwargs):
    kwargs.setdefault('allow_nan', False)
    return json.dump(*args, **kwargs)


@functools.wraps(json.dumps)
def dumps(*args, **kwargs):
    kwargs.setdefault('allow_nan', False)
    return json.dumps(*args, **kwargs)


@functools.wraps(json.load)
def load(*args, **kwargs):
    kwargs.setdefault('parse_constant', strict_constant)
    if kwargs.get('cls') is None:
        # Custom decoder classes may bring their own `parse_float`.
        kwargs.setdefault('parse_float', strict_float)
    return json.load(*args, **kwargs)


@functools.wraps(json.loads)
def loads(*args, **kwargs):
    kwargs.setdefault('parse_constant', strict_constant)
    if kwargs.get('cls') is None:
        # Custom decoder classes may bring their own `parse_float`.
        kwargs.setdefault('parse_float', strict_float)
    return json.loads(*args, **kwargs)

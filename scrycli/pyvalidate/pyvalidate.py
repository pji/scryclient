# -*- coding: utf-8 -*-
"""
pyvalidate
~~~~~~~~~~

This implements the core features of the pyvalidate module.
"""
from collections.abc import Mapping, Sequence
from functools import wraps
from re import match
from urllib.parse import urlparse
from .normalize import from_ctype, from_json, canonicalize, normalize

# Exception messages.
msg = {
    'type': '{} must be of type {}. Was {}.',
    'min': '{} must be at least {}.',
    'max': '{} cannot be more than {}.',
    'minlen': '{} must be longer than {}.',
    'maxlen': '{} must be shorter than {}.',
    'pattern': '{} must match pattern {}.',
    'enum': '{} does not match a value in list.',
    'key': '{} contains an invalid key.',
    'reqkey': '{} is missing required key(s): {}.',
    'value': '{} has invalid value.',
    'novalidate': 'No validator configured for {}.',
}

# Configuration for trust_boundary.
tbvals = {}

# Simple validation.
def isvalid(item, name, validtype, min=None, max=None, minlen=None, 
            maxlen=None, pattern=None, enum=None):
    """A generic validation function for simple data types.
    
    :param item: The item to validate.
    :param name: The name of the validated item. This is used when 
        raising exceptions.
    :param validtype: The valid type for the item.
    :param min: (Optional.) The minimum value for the item.
    :param max: (Optional.) The maximum value for the item.
    :param minlen: (Optional.) The minumum length for the item.
    :param maxlen: (Optional.) The maximum length for the item.
    :param pattern: (Optional.) The regular expression for the item.
    :param enum: (Optional.) A list of values for the item.
    :return: True.
    :rtype: bool.
    
    Usage::
    
        >>> item = 2
        >>> name = 'count'
        >>> validtype = int
        >>> isvalid(item, name, validtype=validtype)
        True
        >>> min = 1
        >>> max = 4
        >>> isvalid(item, name, validtype=validtype, min=min, max=max)
        True
        >>> beatle = {
        ...     'validtype': str,
        ...     'enum': ['John', 'Paul', 'George', 'Ringo'],
        ... }
        >>> item = 'George'
        >>> name = 'Beatle'
        >>> isvalid(item, name, **beatle)
        True
        >>> item2 = 'Mick'
        >>> isvalid(item2, name, **beatle)
        Traceback (most recent call last):
            ...
        ValueError: Beatle does not match a value in list.
    
    """
    if not isinstance(item, validtype):
        raise TypeError(msg['type'].format(name, validtype, type(item)))
    if min:
        if item < min:
            raise ValueError(msg['min'].format(name, min))
    if max:
        if item > max:
            raise ValueError(msg['max'].format(name, max))
    if minlen:
        if len(item) < minlen:
            raise ValueError(msg['minlen'].format(name, minlen))
    if maxlen:
        if len(item) > maxlen:
            raise ValueError(msg['maxlen'].format(name, maxlen))
    if pattern:
        if not match(pattern, item):
            raise ValueError(msg['pattern'].format(name, pattern))
    if enum:
        if item not in enum:
            raise ValueError(msg['enum'].format(name))
    return True


# Complex validation.
def isvalidseq(L, name, val, valkwargs={}):
    """Validate a homogenous sequence of objects.
    
    :param L: The list of items to validate.
    :param name: The name of the list. This is mainly used for 
        exception messages.
    :param val: The validator function to use on the items in 
        the list.
    :param valkwargs: (Optional.) The keyword arguments to pass 
        to the validator.
    :return: True
    :rtype: boolean
    
    Usage::
    
        >>> L = [83, 29, 4, 73, 43]
        >>> name = 'List'
        >>> val = isvalid
        >>> valkwargs = {
        ...     'validtype': int,
        ...     'min': 1,
        ...     'max': 100,
        ... }
        >>> isvalidseq(L, name, val, valkwargs)
        True
    """
    if not isinstance(L, Sequence):
        raise TypeError(msg['type'].format(name, Sequence, type(L)))
    [val(L[i], '{}:{}'.format(name, i), **valkwargs) for i in range(len(L))]
    return True


def isvalidmap(d, name, req={}, opt={}):
    """Validate a mapping.
    
    :param d: The mapping to validate.
    :param name: The name of the mapping. This is mainly used for 
        exception messages.
    :param req: (Optional). The key/value pairs required for 
        the mapping.
    :param opt: (Optional.) The key/value pairs that are optional 
        for the mapping.
    :return: True
    :rtype: boolean
    
    req and opt::
    
        These paramaters describe how to validate each key in the 
        mapping. They must have the following structure:
        
            {
                <valid_key1>: {
                    'val': <validator_function>,
                    'valkwargs': <kwargs_for_validator>,
                },
                <valid_key2>: {
                    'val': <validator_function>,
                    'valkwargs': <kwargs_for_validator>,
                },
                ...       
            }
        
    Usage::
    
        >>> d = {
        ...     'name': 'Terry Jones',
        ...     'type': 'animal',
        ...     'score': 98,
        ... }
        >>> name = 'Python'
        >>> req = {
        ...     'name': {
        ...         'val': isvalid,
        ...         'valkwargs': {
        ...             'validtype': str,
        ...         },
        ...     },
        ...     'type': {
        ...         'val': isvalid,
        ...         'valkwargs': {
        ...             'validtype': str,
        ...             'enum': [
        ...                 'animal',
        ...                 'vegetable',
        ...                 'mineral',
        ...             ],
        ...         },
        ...     },
        ... }
        >>> opt = {
        ...     'score': {
        ...         'val': isvalid,
        ...         'valkwargs': {
        ...             'validtype': int,
        ...             'min': 0,
        ...             'max': 100,
        ...         },
        ...     },
        ... }
        >>> isvalidmap(d, name, req, opt)
        True
    """
    # Test whether d is a mapping.
    if not isinstance(d, Mapping):
        raise TypeError(msg['type'].format(name, Mapping, type(d)))
    
    # Make a defensive copy of req since we're removing values.
    reqcp = req.copy()
    
    # Test each key/value pair in d.
    for key in d:
        newname = '{}:{}'.format(name, key)
        if key in reqcp:
            reqcp[key]['val'](d[key], newname, **reqcp[key]['valkwargs'])
            del(reqcp[key])
        elif key in opt:
            try:
                opt[key]['val'](d[key], newname, **opt[key]['valkwargs'])
            except KeyError:
                raise KeyError(name + ':' + key)
        else:
            raise KeyError(msg['key'].format(name))
    if reqcp:
        raise KeyError(msg['reqkey'].format(name, ', '.join(reqcp.keys())))
    return True


def isvalidurl(s, name, vscheme=None, vnetloc=None, vpath=None, 
          vparams=None, vquery=None, vfrag=None):
    """Validate a url.
    
    :param s: The string to validate.
    :param name: A descriptive name for the URL. This is used for 
        exception messages.
    :param vscheme: (Optional.) The valid scheme for the URL.
    :param vnetloc: (Optional.) The valid net location (domain) for 
        the URL.
    :param vpath: (Optional.) The valid path for the URL.
    :param vparams: (Optional.) The valid parameters for the URL.
    :param vquery: (Optional.) The valid query string for the URL.
    :param vfrag: (Optional.) The valid fragment for the URL.
    :return: True
    :rtype: bool
    """
    # Make sure the value is a string.
    if not isinstance(s, str):
        raise TypeError(msg['type'].format(name, str, type(s)))
    
    # Parse the url into its components.
    url = urlparse(s)
    
    # Validate each relevant part of the url.
    if vscheme:
        if url.scheme != vscheme:
            name += ':{}'.format('scheme')
            raise ValueError(msg['value'].format(name))
    if vnetloc:
        if url.netloc != vnetloc:
            name += ':{}'.format('netloc')
            raise ValueError(msg['value'].format(name))
    if vpath:
        if url.path != vpath:
            name += ':{}'.format('path')
            raise ValueError(msg['value'].format(name))
    if vparams:
        if url.params != vparams:
            name += ':{}'.format('params')
            raise ValueError(msg['value'].format(name))
    if vquery:
        if url.query != vquery:
            name += ':{}'.format('query')
            raise ValueError(msg['value'].format(name))
    if vfrag:
        if url.fragment != vfrag:
            name += ':{}'.format('frag')
            raise ValueError(msg['value'].format(name))
    return True


# Sample validate function.
def validate_httpjson(ctype, content, name, val, valkwargs):
    """A trust boundary validator for the response from a JSON 
    web service.
    
    :param ctype: The text of the Content-Type header from 
        the response.
    :param content: The content from the HTTP response as bytes.
    :param name: The name of the response. Used for exceptions.
    :param validate: The validation function for the content.
    :param valkwargs: The arguments for the validation function.
    :return: The JSON transformed to a list or a dict.
    :rtype: list or dict
    """
    # Configuration setting for the Content-Type validator.
    ctype_valkwargs = {
        'req': {
            'mediatype': {
                'val': isvalid,
                'valkwargs': {
                    'validtype': str,
                    'enum': ['application/json',],
                },
            },
            'charset': {
                'val': isvalid,
                'valkwargs': {
                    'validtype': str,
                    'enum': ['utf-8',],
                },
            },
        },
    }
    
    # Validate ctype.
    canon_ctype = canonicalize(ctype, dest_form='NFC')
    normal_ctype = normalize(canon_ctype, from_ctype)
    isvalidmap(normal_ctype, 'Content-Type', **ctype_valkwargs)
    
    # Validate content.
    enc = normal_ctype['charset']
    canon_content = canonicalize(content, dest_encoding=enc)
    normal_content = normalize(canon_content, from_json)
    val(normal_content, name, **valkwargs)
    return normal_content


# Trust boundary decorator.
def trust_boundary(fn):
    """Marks the existence of a trust boundary between the 
    decorated function and the rest of the script and performs 
    validation on the output of the decorated function.
    
    :param fn: The decorated function.
    :return: The output of the validator for the decorated 
        function.
    :rtype: Varies. See the validator for the decorated function.
    
    Configuration::
    
        trust_boundary uses the following global value to allow 
        consuming scripts to customize it as needed.
        
        :global pyvalidate.tbvals: A dictionary with keys that are 
            the names of the functions wrapped by trust_boundary 
            and values that are the validators for those functions 
            and that validators arguments.
            
                tbvals = {
                    <function1>: {
                        'val': <function1's_validator>,
                        'valkwargs': <function1's_validator's_kwargs>,
                    }
                    <function2>: {
                        'val': <function2's_validator>,
                        'valkwargs': <function2's_validator's_kwargs>,
                    }
                }
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the result of the wrapped function.
        result = fn(*args, **kwargs)
        
        # Find the validator.
        key = fn.__name__
        try:
            validator = tbvals[key]['val']
            valkwargs = tbvals[key]['valkwargs']
        except KeyError:
            raise NotImplementedError(msg['novalidate'].format(key))
        
        # Validate and return the result.
        return validator(*result, key, **valkwargs)
    
    # Return the wrapped function.
    return wrapper
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
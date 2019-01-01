# -*- coding: utf-8 -*-
"""
scrycli
~~~~~~~

This implements the core features of the scrycli module.

:copyright: © 2018 Paul J. Iutzi
:license: MIT, see LICENSE for more details.
"""
from functools import wraps
from json import loads
from json.decoder import JSONDecodeError
from unicodedata import normalize

import requests

from scrycli import config
from scrycli.validator import issetobject

# Global configuration settings.
FQDN = config.fqdn


def trust_boundary(fn):
    """Performs validation at a trust boundary."""
    validators = {'sets': sets_validator,}

    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        try:
            key = fn.__name__
            return validators[key](*result)
        except KeyError:
            raise NotImplementedError('No validator for trust boundary.')
    return wrapper


def sets_validator(ctype: str, content: bytes):
    """Validate the response from Scryfall.com.
    
    :param type: The Content-Type header returned by Scryfall.com. 
    :param content: The content returned from Scryfall.com.
    :return: :class:list
    :rtype: list
    """
    # Canonicalize ctype
    if not isinstance(ctype, str):
        raise TypeError('ctype must be a str. Was: {}'.format(type(ctype)))
    
    # Normalize ctype
    mtype = None
    cset = None
    try:
        ctype_fields = ctype.split('; ')
        mtype = ctype_fields[0]
        cset_fields = ctype_fields[1].split('=')
        cset = cset_fields[1]
    except IndexError:
        raise ValueError('Content-Type must have structure: '
                         '<MIME type>; charset=<character set>')
    
    # Validate ctype
    if mtype != 'application/json':
        raise ValueError('Content-Type must be application/json.')
    if cset != 'utf-8':
        raise ValueError('Character set must be utf-8.')
    
    # Canonicalize content
    if not isinstance(content, bytes):
        raise TypeError('content must be bytes.')
    canon_content = None
    try:
        decoded_content = content.decode('utf_8')
        canon_content = normalize('NFC', decoded_content)
    except UnicodeDecodeError:
        raise ValueError('content must be valid utf-8.')
    
    # Normalize content
    try:
        dict_content = loads(canon_content)
        normal_content = dict_content['data']
    except JSONDecodeError:
        raise ValueError('content must be valid JSON.')
    except KeyError:
        raise ValueError('content must have a key named data.')
    
    # Validate content
    if not isinstance(normal_content, list):
        raise ValueError('Sets must be in a list.')
    for set in normal_content:
        issetobject(set)
    
    return normal_content


@trust_boundary
def sets():
    """Pull a list of sets from Scryfall.com.
    
    :return: :class:str
    :rtype: str
    
    Warning
    -------
    While the return type of the sets() function is a string 
    containing JSON data, calls to set() will get back a 
    list of dictionaries due to the trust_boundary() decorator 
    manipulating the data returned.
    """
    url = FQDN + '/sets'
    resp = requests.get(url)
    return resp.headers['Content-Type'], resp.content


if __name__ == '__main__':
    from pprint import pprint
    pprint(sets())
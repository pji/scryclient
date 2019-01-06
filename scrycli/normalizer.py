# -*- coding: utf-8 -*-
"""
normalizer
~~~~~~~

Provides canonicalization and normalization functions for scrycli module.

:copyright: © 2018 Paul J. Iutzi
:license: MIT, see LICENSE for more details.
"""
from json import loads
from json.decoder import JSONDecodeError
from unicodedata import normalize

# Common exception message strings.
badtype = '{} must be type {}. Was {}.'
baddecode = '{} was not valid {}.'

def canonicalize(text, name, vtype, encoding='utf_8', form='NFC'):
    """Canonicalize text data."""
    canon_text = None
    allowed_types = [str, bytes]
    
    # Ensure proper type before proceeding.
    if vtype not in allowed_types:
        atypestr = str(allowed_types.pop(0))
        for item in allowed_types:
            atypestr += ', {}'.format(item)
        raise TypeError(badtype.format(name, atypestr, vtype))
    
    if not isinstance(text, vtype):
        raise TypeError(badtype.format(name, vtype, type(text)))
    
    # Strings are decoded, and we take that at face value.
    if vtype == str:
        canon_text = text
    
    # Bytes must be decoded and 'normalized' properly.
    elif vtype == bytes:
        try:
            decoded_text = text.decode(encoding)
            canon_text = normalize(form, decoded_text)
        except UnicodeDecodeError:
            raise ValueError(baddecode.format(name, encoding))            
    
    return canon_text


def normalize_ctype(s):
    """Normalize the Content-Type header to a dictionary."""
    ctype = {}
    sfields = s.split(';')[::-1]
    ctype['mediatype'] = sfields.pop().lower()
    while sfields:
        fields = sfields.pop().lstrip().split('=')
        try:
            ctype[fields[0].lower()] = fields[1]
        except IndexError:
            raise ValueError('Content-Type parameters must '
                             'be name=value pairs.')
    return ctype


def normalize_json(json, name: str = 'content', keyfilter: str = None):
    """Normalize a JSON string to Python built-in types."""
    normal = None
    try:
        normal = loads(json)
    except JSONDecodeError:
        msg = '{} must be valid JSON.'.format(name)
        raise ValueError(msg)
    
    if not keyfilter:
        return normal
    elif keyfilter in normal:
        return normal[keyfilter]
    else:
        msg = '{} must have a key named {}.'.format(name, keyfilter)
        raise ValueError(msg)
    
        
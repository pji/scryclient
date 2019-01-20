# -*- coding: utf-8 -*-
"""
normalize
~~~~~~~

Provides canonicalization and normalization functions.

:copyright: © 2018 Paul J. Iutzi
:license: MIT, see LICENSE for more details.
"""
from json import loads
from json.decoder import JSONDecodeError
from unicodedata import normalize as ucd_normalize

# Exception messages.
msg = {
    'type': '{} must be of type {}. Was {}.',
    'decode': '{} was not valid {}.',
}


def canonicalize(text, dest_encoding='utf_8', dest_form='NFC'):
    r"""Canonicalize text data.
    
    :param text: The text to canonicalize.
    :param dest_encoding: (Optional.) The character set to transform 
        the text to. This defaults to UTF-8.
    :param dest_form: (Optional.) The "normal form" to transform the 
        text into. This defaults to NFC.
    :return: The canon text.
    :rtype: str
    
    Usage::
    
        >>> text = b'Montr\xc3\xa9al'
        >>> denc = 'utf_8'
        >>> dform = 'NFC'
        >>> canonicalize(text, dest_encoding=denc, dest_form=dform)
        'Montréal'
    """
    # Decode text and transform to normal form.
    if isinstance(text, bytes):
        try:
            decoded_text = text.decode(dest_encoding)
        except UnicodeDecodeError:
            raise ValueError(msg['decode'].format('Text', dest_encoding))
    else:
        decoded_text = text
    
    # Transform into normal form and return the canon text.
    canon_text = ucd_normalize(dest_form, decoded_text)
    return canon_text


def normalize(item, transform):
    """Normalize data.
    
    :param item: The data to normalize.
    :param transform: The transformation function to run on 
        the data.
    :return: Returns the result of the transform.
    :rtype: Same as the return type of the transform.
    """
    return transform(item)


# Common transform functions.
def from_json(text):
    """Transform json text into a Python object."""
    try:
        return loads(text)
    except JSONDecodeError:
        raise TypeError(msg['decode'].format('Text', 'JSON'))


def from_ctype(text):
    """Transform an HTTP Content-Type header into a dict.
    
    Structure::
    
        The dictionary returned has the following structure:
        
            {
                'mediatype': <response MIME type>,
                'charset': <response character set>,
            }
    """
    ctype = {}
    sfields = text.split(';')[::-1]
    ctype['mediatype'] = sfields.pop().lower()
    while sfields:
        fields = sfields.pop().lstrip().split('=')
        ctype[fields[0]] = fields[1]
    return ctype


if __name__ == '__main__':
    import doctest
    doctest.testmod()
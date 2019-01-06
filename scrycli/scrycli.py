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
from scrycli.validator import iscardlist, issetlist, isdataresp
from scrycli.normalizer import canonicalize, normalize_ctype, normalize_json

# Global configuration settings.
FQDN = config.fqdn
vals = {
    'sets': {
        'keyfilter': 'data',
        'form': 'NFC',
        'mt_val': isdataresp,
        'val': issetlist,
    },
    'cards': {
        'keyfilter': 'data',
        'form': 'NFC',
        'mt_val': isdataresp,
        'val': iscardlist,
    }
}

def trust_boundary(fn):
    """Performs validation at a trust boundary."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        try:
            key = fn.__name__
            return validate(*result, key, **vals[key])
        except KeyError:
            raise NotImplementedError('No validator for trust boundary.')
    return wrapper


def validate(ctype: str, content: bytes, name='response', keyfilter=None, 
             form=None, mt_val=None, val=None):
    """Validate a response from Scryfall.com.
    
    :param ctype: The Content-Type header returned by Scryfall.com.
    :param content: The content returned from Scryfall.com.
    :param name: The name of the response. This is used primarily in 
        error messages.
    :param keyfilter: A key value used to filter unneeded data out of 
        the response.
    :param form: The Unicode normalization form used for 
        canonicalization.
    :param mt_val: The validator function used to validate the media 
        type of the response.
    :param val: The validator function used to validate the content 
        of the response.
    :return: :class:list or :class:dict, depending on the response.
    :rtype: list or dict
    """
    # Handle ctype.
    canon_ctype = canonicalize(ctype, 'Content-Type', str)
    normal_ctype = normalize_ctype(canon_ctype)
    mt_val(normal_ctype)
    
    # Handle content.
    canon_content = canonicalize(content, name, bytes, 
                                 encoding=normal_ctype['charset'], 
                                 form=form)
    normal_content = normalize_json(canon_content, name, keyfilter=keyfilter)
    val(normal_content, name)
    return normal_content


# API calls.
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


@trust_boundary
def cards(page: int = None):
    """Pull a list of cards from Scryfall.com.
    
    :param page: (Optional.) The results page to request from Scryfall.com.
    :return: :class:str
    :rtype: str
    
    Warning
    -------
    While the return type of the sets() function is a string 
    containing JSON data, calls to set() will get back a 
    list of dictionaries due to the trust_boundary() decorator 
    manipulating the data returned.
    """
    url = FQDN + '/cards'
    params = {}
    if page:
        params['page'] = page
    resp = requests.get(url, params)
    return resp.headers['Content-Type'], resp.content


def cards_search(q, unique=None, order=None, dir=None, include_extras=None, 
                 include_multilingual=None, page=None, format=None, 
                 pretty=None):
    """Search the cards in the Scryfall.com database.
    
    :param q: A fulltext search query.
    :param unique: (Optional.) Strategy for omitting similar cards.
    :param order: (Optional.) Sort order for the returned cards.
    :param dir: (Optional.) The direction to sort the returned cards. 
    :param include_extras: (Optional.) Include extra cards, like 
        tokens, to the returned cards.
    :param include_multilingual: (Optional.) If true, will return 
        each language version of each card returned. If missing 
        it defaults to false.
    :param page: (Optional.) Which page of the results to return. 
        If missing, it defaults to 1.
    :param format: (Optional.) Whether to return results in json 
        or csv format. If missing, it defaults to json.
    :param pretty: (Optional.) Asks Scryfall.com to return prettified 
        json. For testing purposes only.
    :return: The content type and response data as a :class:tuple.
    :rtype: tuple
    
    Warning
    -------
    While the return type of the sets() function is a string 
    containing JSON data, calls to set() will get back a 
    list of dictionaries due to the trust_boundary() decorator 
    manipulating the data returned.
    """
    pass


if __name__ == '__main__':
    from pprint import pprint
    #pprint(sets())
    pprint(cards())
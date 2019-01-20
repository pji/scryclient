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
import scrycli.pyvalidate.pyvalidate as PV
import scrycli.pyvalidate.normalize as PN


# Global configuration settings.
FQDN = config.fqdn
PV.tbvals = {
    'sets': {
        'val': PV.validate_httpjson,
        'valkwargs': config.cvals['sf_setlist'],
    },
    'sets_code': {
        'val': PV.validate_httpjson,
        'valkwargs': config.cvals['sf_set'],
    },
    'cards': {
        'val': PV.validate_httpjson,
        'valkwargs': config.cvals['sf_cardlist'],
    },
    'cards_search': {
        'val': PV.validate_httpjson,
        'valkwargs': config.cvals['sf_cardlist'],
    },
}


# Exceptions raised by scrycli.
class HTTPUnknownError(Exception):
    """Raised for unexpected HTTP status codes without another 
    defined exception.
    """

class HTTPRedirectError(Exception):
    """Raised for unexpected HTTP status codes in the 3xx 
    range. This likely means the scrycli needs to be updated.
    """

class HTTPClientError(Exception):
    """Raised for HTTP status codes in the 4xx range. This likely 
    means that you supplied bad input to scrycli.
    """

class HTTPServerError(Exception):
    """Raised for HTTP status codes in the 5xx range. This likely 
    means there is a problem at Scryfall.com's end, but very bad 
    input to scrycli may be able to cause this.
    """


# API calls.
@PV.trust_boundary
def sets():
    """Pull a list of sets from Scryfall.com.
    
    :return: :class:tuple of the Content-Type header and the raw 
        response contents from Scryfall.com
    :rtype: tuple
    
    Warning::
    
        The PV.trust_boundary decorator alters the return type of 
        this function to the PV.validate_httpjson function's 
        return type. That return type will vary based on the 
        data fed into it. In this case it is:
        
        :return: A :class:list of :class:dict that contain the 
            details of each MtG set.
        :rtype: list
    """
    url = FQDN + '/sets'
    resp = _get(url)
    return resp.headers['Content-Type'], resp.content


@PV.trust_boundary
def sets_code(code: str, pretty: bool = False):
    """Get the details for a specific set.
    
    :param code: The three of four letter set code.
    :param pretty: (Optional.) Indicate whether you want the 
        JSON to be returned in a human readable format. Only 
        use for testing.
    :return: :class:tuple of the Content-Type header and the raw 
        response contents from Scryfall.com
    :rtype: tuple
    
    Warning::
    
        The PV.trust_boundary decorator alters the return type of 
        this function to the PV.validate_httpjson function's 
        return type. That return type will vary based on the 
        data fed into it. In this case it is:
        
        :return: A :class:dict that contains the 
            details of a MtG set.
        :rtype: dict
    """
    url = FQDN + '/sets/' + code
    params = {}
    if pretty:
        params['pretty'] = True
    resp = _get(url, params)
    return resp.headers['Content-Type'], resp.content


@PV.trust_boundary
def cards(page: int = None):
    """Pull a list of cards from Scryfall.com.
    
    :param page: (Optional.) The results page to request from Scryfall.com.
    :return: :class:str
    :rtype: str
    
    Warning::
    
        The PV.trust_boundary decorator alters the return type of 
        this function to the PV.validate_httpjson function's 
        return type. That return type will vary based on the 
        data fed into it. In this case it is:
        
        :return: A :class:list of :class:dict that contain the 
            details of each MtG card.
        :rtype: list
    """
    url = FQDN + '/cards'
    params = {}
    if page:
        params['page'] = page
    resp = _get(url, params)
    return resp.headers['Content-Type'], resp.content


@PV.trust_boundary
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
    
    Paging
    ------
    This interface only returns 175 cards at a time, so it will need 
    to make multiple requests to get back all of the data. That will 
    need to be implemented in the client. This call will only return 
    one page at a time. 
    
    Warning::
    
        The PV.trust_boundary decorator alters the return type of 
        this function to the PV.validate_httpjson function's 
        return type. That return type will vary based on the 
        data fed into it. In this case it is:
        
        :return: A :class:dict that contains the results of 
            the search.
        :rtype: dict
    """
    url = FQDN + '/cards/search'
    params = {}
    params['q'] = q
    if unique:
        params['unique'] = unique
    if order:
        params['order'] = order
    if dir:
        params['dir'] = dir
    if include_extras:
        params['include_extras'] = include_extras
    if include_multilingual:
        params['include_multilingual'] = include_multilingual
    if page:
        params['page'] = page
    if format:
        params['format'] = format
    if pretty:
        params['pretty'] = pretty
    resp = _get(url, params)
    return resp.headers['Content-Type'], resp.content


# Private functions.
def _get(url: str, params: dict = {}):
    """Make the HTTP request and handle error responses."""
    resp = requests.get(url, params)
    if resp.status_code != 200:
        msg = '{}: {}'.format(resp.status_code, resp.reason)
        if resp.status_code >= 600:
            raise HTTPUnknownError(msg)
        elif resp.status_code >= 500:
            raise HTTPServerError(msg)
        elif resp.status_code >= 400:
            raise HTTPClientError(msg)
        elif resp.status_code >= 300:
            raise HTTPRedirectError(msg)
        else:
            raise HTTPUnknownError(msg)
    return resp


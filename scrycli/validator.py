# -*- coding: utf-8 -*-
"""
validator
~~~~~~~~~

Common validators for scrycli.
"""
from re import match
from urllib.parse import urlparse

# Common exception messages.
badtype = '{} value must be of type {}.'
badvalue = '{} has invalid value.'


# Simple validators.
def isvalid(o, name, validtype, minlen=None, maxlen=None, pattern=None, 
            enum=None):
    """Generic validation function."""
    if not isinstance(o, validtype):
        raise TypeError(badtype.format(name, validtype))
    if minlen:
        if len(o) < minlen:
            raise ValueError(badvalue.format(name))
    if maxlen:
        if len(o) > maxlen:
            raise ValueError(badvalue.format(name))
    if pattern:
        if not match(pattern, o):
            raise ValueError(badvalue.format(name))
    if enum:
        if o not in enum:
            raise ValueError(badvalue.format(name))
    return True


def isbool(b, name='boolean'):
    """Validate a boolean field."""
    validtype = bool
    return isvalid(b, name, validtype)


def iscard_count(n, name='card_count'):
    """Validate a tcgplayer_id field."""
    validtype = int
    return isvalid(n, name, validtype)


def iscode(s, name='code'):
    """Validate set's code field."""
    validtype = str
    minlen = 2
    maxlen = 6
    return isvalid(s, name, validtype, minlen=minlen, maxlen=maxlen)


def isdate(s, name='date'):
    """Validate a date field."""
    validtype = str
    pattern = '[12][0-9]{3}-[01][0-9]-[0123][0-9]'
    return isvalid(s, name, validtype, pattern=pattern)


def isid(s, name='id'):
    """Validate the id field of a Scryfall.com object."""
    validtype = str
    pattern = ('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-'
                    '[0-9a-f]{12}')
    return isvalid(s, name, validtype, pattern=pattern)


def isname(s, name='name'):
    """Validate a name field."""
    validtype = str
    return isvalid(s, name, validtype)


def isobject(s, name='object'):
    """Validate the object field of a Scryfall.com object."""
    validtype = str
    enum = ['set',]
    return isvalid(s, name, validtype, enum=enum)


def isset_type(s, name='set_type'):
    """Validate a set type field."""
    validtype = str
    enum = ['core', 'expansion', 'masters', 'masterpiece', 'from_the_vault',
            'spellbook', 'premium_deck', 'duel_deck', 'draft_innovation', 
            'treasure_chest', 'commander', 'planechase', 'archenemy', 
            'vanguard', 'funny', 'starter', 'box', 'promo', 'token', 
            'memorabilia']
    return isvalid(s, name, validtype, enum=enum)


def istcgplayer_id(n, name='tcgplayer_id'):
    """Validate a tcgplayer_id field."""
    validtype = int
    return isvalid(n, name, validtype)


# Url validators.
def isurl(s, name='url', vscheme='https', vnetloc=None, vpath=None, 
          vparams=None, vquery=None, vfrag=None):
    """Validate a url."""
    # Make sure the value is a string.
    if not isinstance(s, str):
        raise TypeError(badtype.format(name, str))
    
    # Parse the url into its components.
    url = urlparse(s)
    
    # Validate each relevant part of the url.
    if url.scheme != vscheme:
        raise ValueError(badvalue.format(name))
    if vnetloc:
        if url.netloc != vnetloc:
            raise ValueError(badvalue.format(name))
    if vpath:
        if url.path != vpath:
            raise ValueError(badvalue.format(name))
    if vparams:
        if url.params != vparams:
            raise ValueError(badvalue.format(name))
    if vquery:
        if url.query != vquery:
            raise ValueError(badvalue.format(name))
    if vfrag:
        if url.fragment != vfrag:
            raise ValueError(badvalue.format(name))
    return True


def isapiurl(s, name='api_url'):
    """Validator for the search_uri."""
    vscheme = 'https'
    vnetloc = 'api.scryfall.com'
    return isurl(s, name, vscheme=vscheme, vnetloc=vnetloc)


def isimgurl(s, name='img_url'):
    """Validator for the icon_svg_uri."""
    vscheme = 'https'
    vnetloc = 'img.scryfall.com'
    return isurl(s, name, vscheme=vscheme, vnetloc=vnetloc)


def isscryfallurl(s, name='scryfall_url'):
    """Validator for the search_uri."""
    vscheme = 'https'
    vnetloc = 'scryfall.com'
    return isurl(s, name, vscheme=vscheme, vnetloc=vnetloc)


# Complex validators.
def isvaliddict(d, name: str, s_req: dict = {}, s_opt: dict = {}):
    """Complex validation for dictionaries."""
    if not isinstance(d, dict):
        raise TypeError(badtype.format(name, dict))
    
    # Validate each of the keys.
    for key in d:
        # If it's a required key, validate and cross off the list.
        if key in s_req:
            s_req[key](d[key], key)
            del s_req[key]
        
        # If it's an optional key, just validate
        elif key in s_opt:
            s_opt[key](d[key], key)
        
        # If it's not a required or optional key, it's invalid.
        else:
            raise ValueError(badvalue.format('set object'))
    
    # If any required keys weren't crossed-off, it's invalid.
    if s_req:
        print(s_req)
        raise ValueError(badvalue.format('set object'))
    
    # If everything checks out, return true.
    return True


def issetobject(d, name='set object'):
    """Validation for the scryfall.com set object."""
    s_req = {'object': isobject,
             'id': isid,
             'code': iscode,
             'name': isname,
             'set_type': isset_type,
             'card_count': iscard_count,
             'digital': isbool,
             'foil_only': isbool,
             'icon_svg_uri': isimgurl,
             'search_uri': isapiurl,}
    s_opt = {'tcgplayer_id': istcgplayer_id,
             'released_at': isdate,
             'block_code': iscode,
             'block': isname,
             'uri': isapiurl,
             'scryfall_uri': isscryfallurl,
             'parent_set_code': iscode,
             'mtgo_code': iscode,}
    return isvaliddict(d, name, s_req=s_req, s_opt=s_opt)
            
        
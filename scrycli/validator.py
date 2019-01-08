# -*- coding: utf-8 -*-
"""
validator
~~~~~~~~~

Common validators for scrycli.
"""
from re import match
from urllib.parse import urlparse
from scrycli.utility import parse_manacost

# Common exception messages.
badtype = '{} value must be of type {}.'
badvalue = '{} has invalid value.'

# Keyword args for data validators.
vals = {
    # For isvalid.
    'boolean': {
        'validtype': bool,
    },
    'border': {
        'validtype': str,
        'enum': ['black', 'borderless', 'gold', 'silver', 'white'],
    },
    'code': {
        'validtype': str,
        'minlen': 2,
        'maxlen': 6,
    },
    'color': {
        'validtype': str,
        'enum': ['W', 'U', 'B', 'R', 'G'],
    },
    'component': {
        'validtype': str,
        'enum': ['token', 'meld_part', 'meld_result', 'combo_piece'],
    },
    'date': {
        'validtype': str,
        'pattern': '[12][0-9]{3}-[01][0-9]-[0123][0-9]',
    },
    'decimal': {
        'validtype': (float, int),
    },
    'effect': {
        'validtype': str,
        'enum': ['', 'legendary', 'miracle', 'nyxtouched', 'draft',
                 'devoid', 'tombstone', 'colorshifted', 'sunmoondfc', 
                 'compasslanddfc', 'originpwdfc', 'mooneldrazidfc'],
    },
    'frame': {
        'validtype': str,
        'enum': ['1993', '1997', '2003', '2015', 'future',]
    },
    'games': {
        'validtype': str,
        'enum': ['paper', 'arena', 'mtgo']
    },
    'id': {
        'validtype': str,
        'pattern': ('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-'
                    '[0-9a-f]{12}'),
    },
    'integer': {
        'validtype': int,
    },
    'lang': {
        'validtype': str,
        'enum': [
            'en', 'es', 'fr', 'de', 'it', 'pt', 'ja', 'ko', 'ru', 
            'zhs', 'zht', 'he', 'la', 'grc', 'ar', 'sa', 'px'
        ],
    },
    'layout': {
        'validtype': str,
        'enum': ['normal', 'split', 'flip', 'transform', 'meld',
                 'leveler', 'saga', 'planar', 'scheme', 'vanguard',
                 'token', 'double_faced_token', 'emblem', 'augment',
                 'host'],},
    'legality': {
        'validtype': str,
        'enum': ['legal', 'not_legal', 'restricted', 'banned'],
    },
    'manacost': {
        'validtype': str,
        'enum': [
            '{T}', '{Q}', '{E}', '{PW}', '{CHAOS}', '{X}', '{Y}', '{Z}', 
            '{0}', '{½}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', 
            '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', 
            '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', 
            '{∞}', '{W/U}', '{W/B}', '{B/R}', '{B/G}', '{U/B}', '{U/R}', 
            '{R/G}', '{R/W}', '{G/W}', '{G/U}', '{2/W}', '{2/U}', '{2/B}', 
            '{2/R}', '{2/G}', '{P}', '{W/P}', '{U/P}', '{B/P}', '{R/P}', 
            '{G/P}', '{HW}', '{HR}', '{W}', '{U}', '{B}', '{R}', '{G}', 
            '{C}', '{S}'
        ],
    },
    'modifier': {
        'validtype': str,
        'pattern': '[+-]{1}[0-9]+',
    },
    'object': {
        'validtype': str,
        'enum': ['card', 'card_face', 'related_card', 'set', 'list']
    },
    'rarity': {
        'validtype': str,
        'enum': ['common', 'uncommon', 'rare', 'mythic'],
    },
    'settype': {
        'validtype': str,
        'enum': [
            'core', 'expansion', 'masters', 'masterpiece', 'from_the_vault',
            'spellbook', 'premium_deck', 'duel_deck', 'draft_innovation', 
            'treasure_chest', 'commander', 'planechase', 'archenemy', 
            'vanguard', 'funny', 'starter', 'box', 'promo', 'token', 
            'memorabilia'
        ],
    },
    'text': {
        'validtype': str,
    },
    
    # For isurl.
    'url_api': {
        'vscheme': 'https',
        'vnetloc': 'api.scryfall.com',
    },
    'url_img': {
        'vscheme': 'https',
        'vnetloc': 'img.scryfall.com',
    },
    'url_scry': {
        'vscheme': 'https',
        'vnetloc': 'scryfall.com',
    },
    'url_tcgplayer': {
        'vscheme': 'https',
        'vnetloc': 'shop.tcgplayer.com',
    },
    'url_cardmarket': {
        'vscheme': 'https',
        'vnetloc': 'www.cardmarket.com',
    },
    'url_cardhoarder': {
        'vscheme': 'https',
        'vnetloc': 'www.cardhoarder.com',
    },
    'url_gatherer': {
        'vscheme': 'http',
        'vnetloc': 'gatherer.wizards.com',
    },
    'url_tcgplayerdecks': {
        'vscheme': 'https',
        'vnetloc': 'decks.tcgplayer.com',
    },
    'url_edhrec': {
        'vscheme': 'http',
        'vnetloc': 'edhrec.com',
    },
    'url_mtgtop8': {
        'vscheme': 'http',
        'vnetloc': 'mtgtop8.com',
    },
    
    # For media types.
    'mt_json': {
        'validtype': str,
        'enum': ['application/json'],
    },
    'mt_utf8': {
        'validtype': str,
        'enum': ['utf-8',]
    },
}


# Simple validators.
def isvalid(o, name, validtype=None, minlen=None, maxlen=None, pattern=None, 
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


# Complex validators.
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


def isvaliddict(d, name: str, s_req: dict = {}, s_opt: dict = {},
                c_req: dict = {}, c_opt: dict = {}):
    """Complex validation for dictionaries."""
    if not isinstance(d, dict):
        raise TypeError(badtype.format(name, dict))
    
    # Validate each of the keys.
    for key in d:
        # If it's a required key, validate and cross off the list.
        if key in s_req:
            isvalid(d[key], key, **s_req[key])
            del s_req[key]
        elif key in c_req:
            validator, kwargs = c_req[key]
            validator(d[key], key, **kwargs)
            del c_req[key]
        
        # If it's an optional key, just validate
        elif key in s_opt:
            isvalid(d[key], key, **s_opt[key])
        elif key in c_opt:
            validator, kwargs = c_opt[key]
            validator(d[key], key, **kwargs)
        
        # If it's not a required or optional key, it's invalid.
        else:
            #print(key)
            raise ValueError(badvalue.format(name))
    
    # If any required keys weren't crossed-off, it's invalid.
    if s_req or c_req:
        #print(s_req)
        #print(c_req)
        raise ValueError(badvalue.format(name))
    
    # If everything checks out, return true.
    return True


def isvalidlist(L, name, **kwargs):
    """Complex validation for homogenous lists."""
    if not isinstance(L, list):
        raise TypeError(badtype.format(name, dict))
    [isvalid(item, name, **kwargs) for item in L]
    return True


def isvalidcomplexlist(L, name, validator=None, **kwargs):
    """Complex validation for complex homogenous lists."""
    if not isinstance(L, list):
        raise TypeError(badtype.format(name, list))
    [validator(item, name, **kwargs) for item in L]
    return True


def ismanacostlist(s, name='mana cost'):
    """Validation for the scryfall.com mana cost string."""
    mc = parse_manacost(s)
    return isvalidlist(mc, name, **vals['manacost'])


# Object validators.
def isimageuris(d, name='image uris'):
    """Validator for image_uris."""
    c_opt = {"small": (isurl, vals['url_img']),
             "normal": (isurl, vals['url_img']),
             "large": (isurl, vals['url_img']),
             "png": (isurl, vals['url_img']),
             "art_crop": (isurl, vals['url_img']),
             "border_crop": (isurl, vals['url_img']),}
    return isvaliddict(d, name, c_opt=c_opt)


def iscardfaceobject(d, name='card_face object'):
    """Validation for the scryfall.com card face object."""
    s_req = {'name': vals['text'],
             'object': vals['object'],
             'type_line': vals['text'],}
    s_opt = {'artist': vals['text'],
             'flavor_text': vals['text'],
             'illustration_id': vals['id'],
             'loyalty': vals['text'],
             'oracle_text': vals['text'],
             'power': vals['text'],
             'printed_name': vals['text'],
             'printed_text': vals['text'],
             'printed_type_line': vals['text'],
             'toughness': vals['text'],
             'watermark': vals['text'],}
    c_req = {'mana_cost': (ismanacostlist, {}),}
    c_opt = {'color_indicator': (isvalidlist, vals['color']),
             'colors': (isvalidlist, vals['color']),
             'image_uris': (isimageuris, {}),}
    return isvaliddict(d, name, s_req=s_req, s_opt=s_opt, 
                       c_req=c_req, c_opt=c_opt)


def isrelatedcardobject(d, name='related_card object'):
    """Validation for the scryfall.com related card object."""
    s_req = {'id': vals['id'],
             'object': vals['object'],
             'component': vals['component'],
             'name': vals['text'],
             'type_line': vals['text'],}
    c_req = {'uri': (isurl, vals['url_api']),}
    return isvaliddict(d, name, s_req=s_req, c_req=c_req)
    

def islegalities(d, name='legalities'):
    """Validation for a legalities object."""
    s_req = {'standard': vals['legality'],
             'future': vals['legality'],
             'frontier': vals['legality'],
             'modern': vals['legality'],
             'legacy': vals['legality'],
             'pauper': vals['legality'],
             'vintage': vals['legality'],
             'penny': vals['legality'],
             'commander': vals['legality'],
             '1v1': vals['legality'],
             'duel': vals['legality'],
             'brawl': vals['legality'],}
    return isvaliddict(d, name, s_req=s_req)


def ispurchaseuris(d, name='purchase_uris'):
    """Validation for purchase_uris objects."""
    c_req = {'tcgplayer': (isurl, vals['url_tcgplayer']),
             'cardmarket': (isurl, vals['url_cardmarket']),
             'cardhoarder': (isurl, vals['url_cardhoarder']),}
    return isvaliddict(d, name, c_req=c_req)


def isrelateduris(d, name='related_uris'):
    """Validation for related_uris objects."""
    c_opt = {'gatherer': (isurl, vals['url_gatherer']),
             'tcgplayer_decks': (isurl, vals['url_tcgplayerdecks']),
             'edhrec': (isurl, vals['url_edhrec']),
             'mtgtop8': (isurl, vals['url_mtgtop8']),}
    return isvaliddict(d, name, c_opt=c_opt)


def isset(d, name='set object'):
    """Validation for the scryfall.com set object."""
    s_req = {'object': vals['object'],
             'id': vals['id'],
             'code': vals['code'],
             'name': vals['text'],
             'set_type': vals['settype'],
             'card_count': vals['integer'],
             'digital': vals['boolean'],
             'foil_only': vals['boolean'],}
    s_opt = {'tcgplayer_id': vals['integer'],
             'released_at': vals['date'],
             'block_code': vals['code'],
             'block': vals['text'],
             'parent_set_code': vals['code'],
             'mtgo_code': vals['code'],}
    c_req = {'icon_svg_uri': (isurl, vals['url_img']),
             'search_uri': (isurl, vals['url_api']),}
    c_opt = {'uri': (isurl, vals['url_api']),
             'scryfall_uri': (isurl, vals['url_scry']),}
    return isvaliddict(d, name, s_req=s_req, s_opt=s_opt, 
                       c_req=c_req, c_opt=c_opt)
            

def iscard(d, name='card object'):
    """Validation for the scryfall.com card object."""
    s_req = {'id': vals['id'],
             'lang': vals['lang'],
             'object': vals['object'],
             'oracle_id': vals['id'],
             'cmc': vals['decimal'],
             'foil': vals['boolean'],
             'layout': vals['layout'],
             'name': vals['text'],
             'nonfoil': vals['boolean'],
             'oversized': vals['boolean'],
             'reserved': vals['boolean'],
             'type_line': vals['text'],
             'border_color': vals['border'],
             'collector_number': vals['text'],
             'digital': vals['boolean'],
             'frame': vals['frame'],
             'frame_effect': vals['effect'],
             'full_art': vals['boolean'],
             'highres_image': vals['boolean'],
             'promo': vals['boolean'],
             'rarity': vals['rarity'],
             'released_at': vals['date'],
             'reprint': vals['boolean'],
             'set': vals['code'],
             'set_name': vals['text'],
             'story_spotlight': vals['boolean'],}
    s_opt = {'arena_id': vals['integer'],
             'mtgo_id': vals['integer'],
             'mtgo_foil_id': vals['integer'],
             'tcgplayer_id': vals['integer'],
             'edhrec_rank': vals['integer'],
             'hand_modifier': vals['modifier'],
             'life_modifier': vals['modifier'],
             'loyalty': vals['text'],
             'oracle_text': vals['text'],
             'power': vals['text'],
             'toughness': vals['text'],
             'artist': vals['text'],
             'eur': vals['text'],
             'flavor_text': vals['text'],
             'illustration_id': vals['id'],
             'printed_name': vals['text'],
             'printed_text': vals['text'],
             'printed_type_line': vals['text'],
             'tix': vals['text'],
             'usd': vals['text'],
             'watermark': vals['text'],
             'timeshifted': vals['boolean'],
             'colorshifted': vals['boolean'],
             'futureshifted': vals['boolean'],}
    c_req = {'color_identity': (isvalidlist, vals['color']),
             'prints_search_uri': (isurl, vals['url_api']),
             'rulings_uri': (isurl, vals['url_api']),
             'scryfall_uri': (isurl, vals['url_scry']),
             'uri': (isurl, vals['url_api']),
             'purchase_uris': (ispurchaseuris, {}),
             'related_uris': (isrelateduris, {}),
             'scryfall_set_uri': (isurl, vals['url_scry']),
             'set_search_uri': (isurl, vals['url_api']),
             'games': (isvalidlist, vals['games']),
             'set_uri': (isurl, vals['url_api']),}
    c_opt = {'multiverse_ids': (isvalidlist, vals['integer']),
             'all_parts': (isvalidcomplexlist, 
                           {'validator': isrelatedcardobject,}),
             'card_faces': (isvalidcomplexlist, 
                            {'validator': iscardfaceobject,}),
             'colors': (isvalidlist, vals['color']),
             'color_indicator': (isvalidlist, vals['color']),
             'legalities': (islegalities, {}),
             'mana_cost': (ismanacostlist, {}),
             'image_uris': (isimageuris, {}),}
    try:
        return isvaliddict(d, name, s_req=s_req, s_opt=s_opt, 
                           c_req=c_req, c_opt=c_opt)
    except ValueError as err:
        from pprint import pprint
        pprint(d)
        raise ValueError(str(err))


def isscrylist(d, name='scryfall list', val=None, valkwargs={}):
    """Validator for scryfall.com list objects."""
    s_req = {'object': vals['object'],
             'has_more': vals['boolean'],}
    s_opt = {'total_cards': vals['integer'],}
    c_req = {'data': (val, valkwargs),}
    c_opt = {'next_page': (isurl, vals['url_api']),
             'warnings': (isvalidlist, vals['text']),}
    return isvaliddict(d, name, s_req=s_req, s_opt=s_opt, 
                       c_req=c_req, c_opt=c_opt)


def iscardlist(L, name='cards list'):
    """Validator for a list of set objects."""
    isvalidcomplexlist(L, name, validator=iscard)
    return True


def issetlist(L, name='sets list'):
    """Validator for a list of set objects."""
    isvalidcomplexlist(L, name, validator=isset)
    return True


# Media type validators.
def isdataresp(ctype, name: str = 'data response'):
    """Validate that the Content-Type is correct for a data response 
    from Scryfall.com.
    """
    s_req = {'mediatype': vals['mt_json'],
             'charset': vals['mt_utf8'],}
    return isvaliddict(ctype, name, s_req=s_req)




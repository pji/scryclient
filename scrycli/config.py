# -*- coding: utf-8 -*-
"""
config
~~~~~~

Configuration settings for the scrycli module. It contains the 
following settings:

    url     The url for the Scryfall.com API.
    vals    Validation patterns for Scryfall.com data.
    cvals   Validation patterns for Scryfall.com objects.
    tbvals  Validation configuration for trust boundaries.
"""
from copy import deepcopy
import scrycli.pyvalidate.pyvalidate as PV
import scrycli.utility as U

# The url for the Scryfall.com API.
fqdn = 'https://api.scryfall.com'

# The validation patterns for Scryfall.com data.
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

# Complex validation config for Scryfall.com objects.
cvals = {}
cvals['sf_imageuris'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'opt': {
            "small": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_img'],
            },
            "normal": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_img'],
            },
            "large": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_img'],
            },
            "png": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_img'],
            },
            "art_crop": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_img'],
            },
            "border_crop": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_img'],
            },
        },
    },
}
cvals['sf_cardface'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            'name': {
                'val': PV.isvalid,
                'valkwargs': vals['text'],
            },
            'object': {
                'val': PV.isvalid,
                'valkwargs': vals['object'],
            },
            'type_line': {
                'val': PV.isvalid,
                'valkwargs': vals['text'],
            },
            'mana_cost': {
                'val': U.ismanacostlist,
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['manacost'],
                },
            },
        },
        'opt': {
            'artist': {
                'val': PV.isvalid,
                'valkwargs': vals['text'],
            },
            'flavor_text': {
                'val': PV.isvalid,
                'valkwargs': vals['text'],
            },
            'illustration_id': {
                'val': PV.isvalid,
                'valkwargs': vals['id'],
            },
            'loyalty': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'oracle_text': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'power': {
                'val': PV.isvalid,
                'valkwargs': vals['text'],
            },
            'printed_name': {
                'val': PV.isvalid,
                'valkwargs': vals['text'],
            },
            'printed_text': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'printed_type_line': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'toughness': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'watermark': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'color_indicator': {
                'val': PV.isvalidseq,
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['color'],
                },
            },
            'colors': {
                'val': PV.isvalidseq,
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['color'],
                },
            },
            'image_uris': cvals['sf_imageuris'],
        },
    },
}
cvals['sf_relatedcard'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            'id': {
                'val': PV.isvalid, 
                'valkwargs': vals['id'],
            },
            'object': {
                'val': PV.isvalid, 
                'valkwargs': vals['object'],
            },
            'component': {
                'val': PV.isvalid, 
                'valkwargs': vals['component'],
            },
            'name': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'type_line': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'uri': {
                'val': PV.isvalidurl,
                'valkwargs': vals['url_api'],
            },
        },
    },
}
cvals['sf_legalities'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            'standard': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'future': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'frontier': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'modern': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'legacy': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'pauper': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'vintage': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'penny': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'commander': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            '1v1': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'duel': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
            'brawl': {
                'val': PV.isvalid, 
                'valkwargs': vals['legality'],
            },
        },
    },
}
cvals['sf_purchaseuris'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            "tcgplayer": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_tcgplayer'],
            },
            "cardmarket": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_cardmarket'],
            },
            "cardhoarder": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_cardhoarder'],
            },
        },
    },
}
cvals['sf_relateduris'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'opt': {
            "gatherer": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_gatherer'],
            },
            "tcgplayer_decks": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_tcgplayerdecks'],
            },
            "edhrec": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_edhrec'],
            },
            "mtgtop8": {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_mtgtop8'],
            },
        },
    },
}
cvals['sf_set'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            'object': {
                'val': PV.isvalid, 
                'valkwargs': vals['object'],
            },
            'id': {
                'val': PV.isvalid, 
                'valkwargs': vals['id'],
            },
            'code': {
                'val': PV.isvalid, 
                'valkwargs': vals['code'],
            },
            'name': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'set_type': {
                'val': PV.isvalid, 
                'valkwargs': vals['settype'],
            },
            'card_count': {
                'val': PV.isvalid, 
                'valkwargs': vals['integer'],
            },
            'digital': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'foil_only': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'icon_svg_uri': {
                'val': PV.isvalidurl,
                'valkwargs': vals['url_img'],
            },
            'search_uri': {
                'val': PV.isvalidurl,
                'valkwargs': vals['url_api'],
            },
        },
        'opt': {
            'tcgplayer_id': {
                'val': PV.isvalid, 
                'valkwargs': vals['integer'],
            },
            'released_at': {
                'val': PV.isvalid, 
                'valkwargs': vals['date'],
            },
            'block_code': {
                'val': PV.isvalid, 
                'valkwargs': vals['code'],
            },
            'block': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'parent_set_code': {
                'val': PV.isvalid, 
                'valkwargs': vals['code'],
            },
            'mtgo_code': {
                'val': PV.isvalid, 
                'valkwargs': vals['code'],
            },
            'uri': {
                'val': PV.isvalidurl,
                'valkwargs': vals['url_api'],
            },
            'scryfall_uri': {
                'val': PV.isvalidurl,
                'valkwargs': vals['url_scry'],
            },
        },
    },
}
cvals['sf_card'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            'id': {
                'val': PV.isvalid, 
                'valkwargs': vals['id'],
            },
            'lang': {
                'val': PV.isvalid, 
                'valkwargs': vals['lang'],
            },
            'object': {
                'val': PV.isvalid, 
                'valkwargs': vals['object'],
            },
            'oracle_id': {
                'val': PV.isvalid, 
                'valkwargs': vals['id'],
            },
            'cmc': {
                'val': PV.isvalid, 
                'valkwargs': vals['decimal'],
            },
            'foil': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'layout': {
                'val': PV.isvalid, 
                'valkwargs': vals['layout'],
            },
            'name': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'nonfoil': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'oversized': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'reserved': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'type_line': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'border_color': {
                'val': PV.isvalid, 
                'valkwargs': vals['border'],
            },
            'collector_number': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'digital': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'frame': {
                'val': PV.isvalid, 
                'valkwargs': vals['frame'],
            },
            'frame_effect': {
                'val': PV.isvalid, 
                'valkwargs': vals['effect'],
            },
            'full_art': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'highres_image': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'promo': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'rarity': {
                'val': PV.isvalid, 
                'valkwargs': vals['rarity'],
            },
            'released_at': {
                'val': PV.isvalid, 
                'valkwargs': vals['date'],
            },
            'reprint': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'set': {
                'val': PV.isvalid, 
                'valkwargs': vals['code'],
            },
            'set_name': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'story_spotlight': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'color_identity': {
                'val': PV.isvalidseq, 
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['color'],
                },
            },
            'prints_search_uri': {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_api'],
            },
            'rulings_uri': {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_api'],
            },
            'scryfall_uri': {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_scry'],
            },
            'uri': {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_api'],
            },
            'purchase_uris': cvals['sf_purchaseuris'],
            'related_uris': cvals['sf_relateduris'],
            'scryfall_set_uri': {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_scry'],
            },
            'set_search_uri': {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_api'],
            },
            'games': {
                'val': PV.isvalidseq, 
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['games'],
                },
            },
            'set_uri': {
                'val': PV.isvalidurl, 
                'valkwargs': vals['url_api'],
            },
        },
        'opt': {
            'arena_id': {
                'val': PV.isvalid, 
                'valkwargs': vals['integer'],
            },
            'mtgo_id': {
                'val': PV.isvalid, 
                'valkwargs': vals['integer'],
            },
            'mtgo_foil_id': {
                'val': PV.isvalid, 
                'valkwargs': vals['integer'],
            },
            'tcgplayer_id': {
                'val': PV.isvalid, 
                'valkwargs': vals['integer'],
            },
            'edhrec_rank': {
                'val': PV.isvalid, 
                'valkwargs': vals['integer'],
            },
            'hand_modifier': {
                'val': PV.isvalid, 
                'valkwargs': vals['modifier'],
            },
            'life_modifier': {
                'val': PV.isvalid, 
                'valkwargs': vals['modifier'],
            },
            'loyalty': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'oracle_text': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'power': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'toughness': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'artist': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'eur': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'flavor_text': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'illustration_id': {
                'val': PV.isvalid, 
                'valkwargs': vals['id'],
            },
            'printed_name': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'printed_text': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'printed_type_line': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'tix': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'usd': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'watermark': {
                'val': PV.isvalid, 
                'valkwargs': vals['text'],
            },
            'timeshifted': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'colorshifted': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'futureshifted': {
                'val': PV.isvalid, 
                'valkwargs': vals['boolean'],
            },
            'multiverse_ids': {
                'val': PV.isvalidseq, 
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['integer'],
                },
            },
            'all_parts': {
                'val': PV.isvalidseq,
                'valkwargs': cvals['sf_relatedcard'],
            },
            'card_faces': {
                'val': PV.isvalidseq,
                'valkwargs': cvals['sf_cardface'],
            },
            'colors': {
                'val': PV.isvalidseq, 
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['color'],
                },
            },
            'color_indicator': {
                'val': PV.isvalidseq, 
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['color'],
                },
            },
            'legalities': cvals['sf_legalities'],
            'mana_cost': {
                'val': U.ismanacostlist, 
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['manacost'],
                }
            },
            'image_uris': cvals['sf_imageuris'],
        },
    },
}
cvals['sf_list'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            'object': {
                'val': PV.isvalid,
                'valkwargs': vals['object'],
            },
            'has_more': {
                'val': PV.isvalid,
                'valkwargs': vals['boolean'],
            },
            'data': None,
        },
        'opt': {
            'total_cards': {
                'val': PV.isvalid,
                'valkwargs': vals['integer'],
            },
            'next_page': {
                'val': PV.isvalidurl,
                'valkwargs': vals['url_api'],
            },
            'warnings': {
                'val': PV.isvalidseq,
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['text'],
                },
            },
        },
    },
}
cvals['sf_setlist'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            'object': {
                'val': PV.isvalid,
                'valkwargs': vals['object'],
            },
            'has_more': {
                'val': PV.isvalid,
                'valkwargs': vals['boolean'],
            },
            'data': {
                'val': PV.isvalidseq,
                'valkwargs': cvals['sf_set'],
            },
        },
        'opt': {
            'total_cards': {
                'val': PV.isvalid,
                'valkwargs': vals['integer'],
            },
            'next_page': {
                'val': PV.isvalidurl,
                'valkwargs': vals['url_api'],
            },
            'warnings': {
                'val': PV.isvalidseq,
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['text'],
                },
            },
        },
    },
}
cvals['sf_cardlist'] = {
    'val': PV.isvalidmap,
    'valkwargs': {
        'req': {
            'object': {
                'val': PV.isvalid,
                'valkwargs': vals['object'],
            },
            'has_more': {
                'val': PV.isvalid,
                'valkwargs': vals['boolean'],
            },
            'data': {
                'val': PV.isvalidseq,
                'valkwargs': cvals['sf_card'],
            },
        },
        'opt': {
            'total_cards': {
                'val': PV.isvalid,
                'valkwargs': vals['integer'],
            },
            'next_page': {
                'val': PV.isvalidurl,
                'valkwargs': vals['url_api'],
            },
            'warnings': {
                'val': PV.isvalidseq,
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': vals['text'],
                },
            },
        },
    },
}
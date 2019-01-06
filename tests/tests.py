# -*- coding: utf-8 -*-
"""
tests
~~~~~

Implements the unit tests for the scrycli module.

Run from module root with:
python3 -m unittest tests/tests.py
"""

from json import loads
from threading import Thread
from time import sleep
import unittest

from requests import get

from tests import scryfake
from scrycli import normalizer, scrycli, utility, validator

# Global configuration settings.
FQDN = None
SCRYFAKE_FQDN = 'http://127.0.0.1:5000'

# Common exception messages.
badtype = '{} value must be of type {}.'
badvalue = '{} has invalid value.'


class NormalizerTestCase(unittest.TestCase):
    """Unit tests for scrycli.normalizer.py."""
    def test_canonicalize_HappyStr(self):
        """Happy path str test for canonicalize()."""
        text = 'application/json; charset=utf-8'
        name = 'Content-Type'
        vtype = str
        expected = 'application/json; charset=utf-8'
        self.assertTrue(normalizer.canonicalize(text, name, vtype) 
                        == expected)
    
    def test_canonicalize_HappyBytes(self):
        """Happy path bytes test for canonicalize()."""
        text = b'Montr\xc3\xa9al'
        name = 'city'
        vtype = bytes
        expected = 'Montréal'
        self.assertTrue(normalizer.canonicalize(text, name, vtype) 
                        == expected)
    
    def test_canonicalize_BadVtype(self): 
        text = 'application/json; charset=utf-8'
        name = 'Content-Type'
        vtype = list
        ex = TypeError
        pattern = '{} must be.*Was {}[.]'.format(name, vtype)
        self.assertRaisesRegex(ex, pattern, normalizer.canonicalize, 
                               text, name, vtype)

    def test_canonicalize_TypeMismatch(self): 
        text = b'application/json; charset=utf-8'
        name = 'Content-Type'
        vtype = str
        ex = TypeError
        pattern = '{} must be.*Was {}[.]'.format(name, bytes)
        self.assertRaisesRegex(ex, pattern, normalizer.canonicalize, 
                               text, name, vtype)

    def test_canonicalize_BadCharacter(self): 
        text = b'Montr\xe9al'
        name = 'city'
        vtype = bytes
        encoding = 'utf_8'
        ex = ValueError
        pattern = '{} was not valid {}[.]'.format(name, encoding)
        self.assertRaisesRegex(ex, pattern, normalizer.canonicalize, 
                               text, name, vtype, encoding=encoding)

    def test_canonicalize_BadForm(self): 
        text = b'Montr\xc3\xa9al'
        name = 'city'
        vtype = bytes
        encoding = 'utf_8'
        form = 'XXX'
        ex = ValueError
        pattern = 'invalid normalization form'
        self.assertRaisesRegex(ex, pattern, normalizer.canonicalize, 
                               text, name, vtype, encoding=encoding, 
                               form=form)


class ScrycliTestCase(unittest.TestCase):
    """Unit tests for scrycli.py."""
    @classmethod
    def setUpClass(cls):
        """Stand up test instances and data."""
        # Point scrycli at the scryfake.
        global FQDN
        FQDN = scrycli.FQDN
        scrycli.FQDN = SCRYFAKE_FQDN
        
        # Scryfake halts execution if run in same thread.
        T = Thread(target=scryfake.app.run)
        T.start()
        
        # Wait for Scryfall to finish initializing.
        sleep(.25)        
    
    
    # Tests for sets().
    def test_sets(self):
        """Unit test for the scrycli.sets."""
        #expected = ('application/json; charset=utf-8', scryfake.resp['sets'])
        resp = scryfake.resp['sets']
        expected = loads(resp)['data']
        self.assertEqual(scrycli.sets(), expected)
    
    
    # Tests for validate().
    def test_validate(self):
        """Happy test for scrycli.validate()."""
        args = (
            'application/json; charset=utf-8',
            scryfake.resp['sets'],
        )
        kwargs = {
            'name': 'sets',
            'keyfilter': 'data',
            'form': 'NFC',
            'mt_val': validator.isdataresp,
            'val': validator.issetlist,
        }
        expected = loads(args[1])['data']
        self.assertTrue(scrycli.validate(*args, **kwargs) == expected)
    
    def test_validate_ContentIsList(self):
        """Test if content is wrong type."""
        args = (
            'application/json; charset=utf-8',
            [1, 2],
        )
        kwargs = {
            'name': 'sets',
            'keyfilter': 'data',
            'form': 'NFC',
            'mt_val': validator.isdataresp,
            'val': validator.issetlist,
        }
        regex = '{} must be type {}[.] Was {}[.]'.format(kwargs['name'], 
                                                         bytes, list)
        self.assertRaisesRegex(TypeError, regex, scrycli.validate,
                               *args, **kwargs)
    
    def test_validate_ContentBadChar(self):
        """Test if content has non-utf-8 code point."""
        args = (
            'application/json; charset=utf-8',
            b'Montr\xe9al',
        )
        kwargs = {
            'name': 'sets',
            'keyfilter': 'data',
            'form': 'NFC',
            'mt_val': validator.isdataresp,
            'val': validator.issetlist,
        }
        regex = '{} was not valid {}.'.format(kwargs['name'], 'utf-8')
        self.assertRaisesRegex(ValueError, regex, scrycli.validate,
                               *args, **kwargs)
    
    def test_validate_ContentNotJSON(self):
        """Test if content is not JSON."""
        args = (
            'application/json; charset=utf-8',
            b'{foo]',
        )
        kwargs = {
            'name': 'sets',
            'keyfilter': 'data',
            'form': 'NFC',
            'mt_val': validator.isdataresp,
            'val': validator.issetlist,
        }
        regex = '{} must be valid JSON.'.format(kwargs['name'])
        self.assertRaisesRegex(ValueError, regex, scrycli.validate,
                               *args, **kwargs)
    
    def test_validate_ContentNoDataKey(self):
        """Test if content doesn't have keyfilter."""
        args = (
            'application/json; charset=utf-8',
            b'{"object": "list", "has_more": false}',
        )
        kwargs = {
            'name': 'sets',
            'keyfilter': 'data',
            'form': 'NFC',
            'mt_val': validator.isdataresp,
            'val': validator.issetlist,
        }
        regex = '{} must have a key named {}.'.format(kwargs['name'], 
                                                      kwargs['keyfilter'])
        self.assertRaisesRegex(ValueError, regex, scrycli.validate,
                               *args, **kwargs)
    
    def test_validate_ContentBadType(self):
        """Test if content doesn't have keyfilter."""
        args = (
            'application/json; charset=utf-8',
            b'{"object": "list", "has_more": false, "data": "hi"}',
        )
        kwargs = {
            'name': 'sets',
            'keyfilter': 'data',
            'form': 'NFC',
            'mt_val': validator.isdataresp,
            'val': validator.issetlist,
        }
        regex = '{} value must be of type {}.'.format(kwargs['name'], list)
        self.assertRaisesRegex(TypeError, regex, scrycli.validate,
                               *args, **kwargs)
    
    
    # Tests for cards().
    def test_cards(self):
        """Unit tests for cards()."""
        resp = scryfake.resp['cards']
        expected = loads(resp)['data']
        self.assertEqual(scrycli.cards(), expected)
    
    @classmethod
    def tearDownClass(cls):
        """Tear down test instances and data."""
        # Shutdown the Scryfake instance.
        get('http://127.0.0.1:5000/shutdown')
        
        # Point scrycli back at Scryfall.com just in case.
        global FQDN
        scrycli.FQDN = FQDN
        FQDN = None


class UtilityTestCase(unittest.TestCase):
    """Unit tests for utility.py."""
    def test_build_query(self):
        """Unit test for utility.build_query()."""
        kwargs = {'cardset': 'rna'}
        expected = 'set:rna '
        self.assertEqual(utility.build_query(**kwargs), expected)
    
    def test_parse_manacost(self):
        """Unit tests for utility.parse_manacost(s)."""
        s = '{2}{W}{U}'
        expected = ['{2}', '{W}', '{U}']
        self.assertEqual(utility.parse_manacost(s), expected)


class ValidatorTestCase(unittest.TestCase):
    """Unit tests for validator."""
    def test_isurl(self):
        """Tests for isurl(s)."""
        s = 'https://api.scryfall.com/sets'
        vscheme = 'https'
        vnetloc = 'api.scryfall.com'
        vpath = '/sets'
        self.assertTrue(validator.isurl(s, vscheme=vscheme, vnetloc=vnetloc, 
                                        vpath=vpath))
        
        # Not a str.
        s = [1, 2]
        regex = badtype.format('url', str)
        self.assertRaisesRegex(TypeError, regex, validator.isurl, s)
        
        # Not a valid scheme.
        s = 'ftp://test.test'
        vscheme = 'https'
        regex = badvalue.format('url')
        self.assertRaisesRegex(ValueError, regex, validator.isurl, 
                               s, vscheme=vscheme)
        
        # Not a valid netloc
        s = 'ftp://test.test'
        vnetloc = 'api.scryfall.com'
        regex = badvalue.format('url')
        self.assertRaisesRegex(ValueError, regex, validator.isurl, 
                               s, vnetloc=vnetloc)
    
        
    def test_isvalidlist(self):
        """Unit tests for isvalidlist(L, name)."""
        L = [11112, 14532, 86543, 75432]
        name = 'list'
        v = validator.vals['integer']
        self.assertTrue(validator.isvalidlist(L, name, **v))
        
        L = ['hi', 14532, 86543, 75432]
        name = 'list'
        v = validator.vals['integer']
        regex = badtype.format(name, int)
        self.assertRaisesRegex(TypeError, regex, validator.isvalidlist, 
                               L, name, **v)        
    
    
    def test_isset(self):
        """Tests for issetobject()."""
        d = {
              "object": "set",
              "id": "ee3a8eb6-0583-492b-8be5-265795d38038",
              "code": "prw2",
              "name": "RNA Ravnica Weekend",
              "uri": "https://api.scryfall.com/sets/prw2",
              "scryfall_uri": "https://scryfall.com/sets/prw2",
              "search_uri": ("https://api.scryfall.com/cards/search?"
                             "order=set&q=e%3Aprw2&unique=prints"),
              "released_at": "2019-02-16",
              "set_type": "promo",
              "card_count": 10,
              "parent_set_code": "rna",
              "digital": False,
              "foil_only": False,
              "icon_svg_uri": "https://img.scryfall.com/sets/rna.svg?1545627600"
            }
        self.assertTrue(validator.isset(d))

    
    def test_isimageuris(self):
        """Tests for isimageuris()."""
        d = {"small": ("https://img.scryfall.com/cards/small/front/f/f/"
                       "ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg?1545071267"),
             "normal": ("https://img.scryfall.com/cards/normal/front/f/f/"
                        "ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg?1545071267"),
             "large": ("https://img.scryfall.com/cards/large/front/f/f/"
                       "ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg?1545071267"),
             "png": ("https://img.scryfall.com/cards/png/front/f/f/"
                     "ff782973-e33c-4edd-bbd7-5c8dc8d59554.png?1545071267"),
             "art_crop": ("https://img.scryfall.com/cards/art_crop/front/f/f/"
                          "ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg"
                          "?1545071267"),
             "border_crop": ("https://img.scryfall.com/cards/border_crop/"
                             "front/f/f/ff782973-e33c-4edd-bbd7-5c8dc8d59554."
                             "jpg?1545071267"),}
        self.assertTrue(validator.isimageuris(d))
    
    
    def test_ismanacostlist(self):
        """Tests for ismanacostlist(s)."""
        s = '{2}{W}{U}'
        self.assertTrue(validator.ismanacostlist(s))
        
        s = ''
        self.assertTrue(validator.ismanacostlist(s))
    
    
    def test_iscardfaceobject(self):
        """Tests for iscardfaceobject(d)."""
        d = {"object": "card_face",
             "name": "Golden Guardian",
             "mana_cost": "{4}",
             "type_line": "Artifact Creature — Golem",
             "oracle_text": ("Defender\n{2}: Golden Guardian fights another "
                             "target creature you control. When Golden "
                             "Guardian dies this turn, return it to the "
                             "battlefield transformed under your control."),
             "colors": [],
             "power": "4",
             "toughness": "4",
             "artist": "Svetlin Velinov",
             "illustration_id": "6fdeefae-2e81-44dc-b337-88079c0494d9",
             "image_uris": {
                "small": ("https://img.scryfall.com/cards/small/en/rix/"
                          "179a.jpg?1524752577"),
                "normal": ("https://img.scryfall.com/cards/normal/en/rix/"
                           "179a.jpg?1524752577"),
                "large": ("https://img.scryfall.com/cards/large/en/rix/"
                          "179a.jpg?1524752577"),
                "png": ("https://img.scryfall.com/cards/png/en/rix/"
                        "179a.png?1524752577"),
                "art_crop": ("https://img.scryfall.com/cards/art_crop/en/"
                             "rix/179a.jpg?1524752577"),
                "border_crop": ("https://img.scryfall.com/cards/border_crop/"
                                "en/rix/179a.jpg?1524752577"),
                },
            }
        self.assertTrue(validator.iscardfaceobject(d))
    
    
    def test_isrelatedcardobject(self):
        """Tests for issetobject()."""
        d = {"object": "related_card",
             "id": "0900e494-962d-48c6-8e78-66a489be4bb2",
             "component": "meld_part",
             "name": "Hanweir Garrison",
             "type_line": "Creature — Human Soldier",
             "uri": ("https://api.scryfall.com/cards/"
                     "0900e494-962d-48c6-8e78-66a489be4bb2"),}
        self.assertTrue(validator.isrelatedcardobject(d))
    
    
    def test_iscard(self):
        """Tests for iscard()."""
        d = {
              "object": "card",
              "id": "0900e494-962d-48c6-8e78-66a489be4bb2",
              "oracle_id": "7cb29569-48e1-4782-9906-fad155ebfafe",
              "multiverse_ids": [
                414428
              ],
              "mtgo_id": 61220,
              "tcgplayer_id": 119682,
              "name": "Hanweir Garrison",
              "lang": "en",
              "released_at": "2016-07-22",
              "uri": "https://api.scryfall.com/cards/0900e494-962d-48c6-8e78-66a489be4bb2",
              "scryfall_uri": "https://scryfall.com/card/emn/130a/hanweir-garrison?utm_source=api",
              "layout": "meld",
              "highres_image": True,
              "image_uris": {
                "small": "https://img.scryfall.com/cards/small/en/emn/130a.jpg?1526595227",
                "normal": "https://img.scryfall.com/cards/normal/en/emn/130a.jpg?1526595227",
                "large": "https://img.scryfall.com/cards/large/en/emn/130a.jpg?1526595227",
                "png": "https://img.scryfall.com/cards/png/en/emn/130a.png?1526595227",
                "art_crop": "https://img.scryfall.com/cards/art_crop/en/emn/130a.jpg?1526595227",
                "border_crop": "https://img.scryfall.com/cards/border_crop/en/emn/130a.jpg?1526595227"
              },
              "mana_cost": "{2}{R}",
              "cmc": 3.0,
              "type_line": "Creature — Human Soldier",
              "oracle_text": "Whenever Hanweir Garrison attacks, create two 1/1 red Human creature tokens that are tapped and attacking.\n(Melds with Hanweir Battlements.)",
              "power": "2",
              "toughness": "3",
              "colors": [
                "R"
              ],
              "color_identity": [
                "R"
              ],
              "all_parts": [
                {
                  "object": "related_card",
                  "id": "0900e494-962d-48c6-8e78-66a489be4bb2",
                  "component": "meld_part",
                  "name": "Hanweir Garrison",
                  "type_line": "Creature — Human Soldier",
                  "uri": "https://api.scryfall.com/cards/0900e494-962d-48c6-8e78-66a489be4bb2"
                },
                {
                  "object": "related_card",
                  "id": "671fe14d-0070-4bc7-8983-707b570f4492",
                  "component": "meld_result",
                  "name": "Hanweir, the Writhing Township",
                  "type_line": "Legendary Creature — Eldrazi Ooze",
                  "uri": "https://api.scryfall.com/cards/671fe14d-0070-4bc7-8983-707b570f4492"
                },
                {
                  "object": "related_card",
                  "id": "1d743ad6-6ca2-409a-9773-581cc195dbf2",
                  "component": "meld_part",
                  "name": "Hanweir Battlements",
                  "type_line": "Land",
                  "uri": "https://api.scryfall.com/cards/1d743ad6-6ca2-409a-9773-581cc195dbf2"
                },
                {
                  "object": "related_card",
                  "id": "dbd994fc-f3f0-4c81-86bd-14ca63ec229b",
                  "component": "token",
                  "name": "Human",
                  "type_line": "Token Creature — Human",
                  "uri": "https://api.scryfall.com/cards/dbd994fc-f3f0-4c81-86bd-14ca63ec229b"
                }
              ],
              "legalities": {
                "standard": "not_legal",
                "future": "not_legal",
                "frontier": "legal",
                "modern": "legal",
                "legacy": "legal",
                "pauper": "not_legal",
                "vintage": "legal",
                "penny": "not_legal",
                "commander": "legal",
                "1v1": "legal",
                "duel": "legal",
                "brawl": "not_legal"
              },
              "games": [
                "mtgo",
                "paper"
              ],
              "reserved": False,
              "foil": True,
              "nonfoil": True,
              "oversized": False,
              "promo": False,
              "reprint": False,
              "set": "emn",
              "set_name": "Eldritch Moon",
              "set_uri": "https://api.scryfall.com/sets/5f0e4093-334f-4439-bbb5-a0affafd0ffc",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aemn&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/emn?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/0900e494-962d-48c6-8e78-66a489be4bb2/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A7cb29569-48e1-4782-9906-fad155ebfafe&unique=prints",
              "collector_number": "130a",
              "digital": False,
              "rarity": "rare",
              "flavor_text": "\"We're ready for anything!\"",
              "illustration_id": "2b2d858a-8c54-413a-a107-cfc587540ac9",
              "artist": "Vincent Proce",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": False,
              "story_spotlight": False,
              "edhrec_rank": 946,
              "usd": "1.29",
              "tix": "0.01",
              "related_uris": {
                "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=414428",
                "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Hanweir+Garrison&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "edhrec": "http://edhrec.com/route/?cc=Hanweir+Garrison",
                "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Hanweir+Garrison"
              },
              "purchase_uris": {
                "tcgplayer": "https://shop.tcgplayer.com/magic/eldritch-moon/hanweir-garrison?partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "cardmarket": "https://www.cardmarket.com/en/Magic?mainPage=showSearchResult&referrer=scryfall&searchFor=Hanweir+Garrison",
                "cardhoarder": "https://www.cardhoarder.com/cards/61220?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
              }
            }
        self.assertTrue(validator.iscard(d))
    
    
    def test_iscardlist(self):
        """Tests for iscardlist()."""
        d = [
            {
              "object": "card",
              "id": "9472cd09-0b0a-49c9-ab10-ec5b73ddb74b",
              "oracle_id": "2aa0e0e5-cb6d-4518-8eff-d29f935486e0",
              "multiverse_ids": [
                456771
              ],
              "mtgo_id": 70423,
              "tcgplayer_id": 180973,
              "name": "Nourishing Shoal",
              "lang": "en",
              "released_at": "2018-12-07",
              "uri": "https://api.scryfall.com/cards/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b",
              "scryfall_uri": "https://scryfall.com/card/uma/175/nourishing-shoal?utm_source=api",
              "layout": "normal",
              "highres_image": False,
              "image_uris": {
                "small": "https://img.scryfall.com/cards/small/front/9/4/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b.jpg?1542806319",
                "normal": "https://img.scryfall.com/cards/normal/front/9/4/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b.jpg?1542806319",
                "large": "https://img.scryfall.com/cards/large/front/9/4/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b.jpg?1542806319",
                "png": "https://img.scryfall.com/cards/png/front/9/4/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b.png?1542806319",
                "art_crop": "https://img.scryfall.com/cards/art_crop/front/9/4/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b.jpg?1542806319",
                "border_crop": "https://img.scryfall.com/cards/border_crop/front/9/4/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b.jpg?1542806319"
              },
              "mana_cost": "{X}{G}{G}",
              "cmc": 2,
              "type_line": "Instant — Arcane",
              "oracle_text": "You may exile a green card with converted mana cost X from your hand rather than pay this spell's mana cost.\nYou gain X life.",
              "colors": [
                "G"
              ],
              "color_identity": [
                "G"
              ],
              "legalities": {
                "standard": "not_legal",
                "future": "not_legal",
                "frontier": "not_legal",
                "modern": "legal",
                "legacy": "legal",
                "pauper": "not_legal",
                "vintage": "legal",
                "penny": "not_legal",
                "commander": "legal",
                "1v1": "legal",
                "duel": "legal",
                "brawl": "not_legal"
              },
              "games": [
                "mtgo",
                "paper"
              ],
              "reserved": False,
              "foil": True,
              "nonfoil": True,
              "oversized": False,
              "promo": False,
              "reprint": True,
              "set": "uma",
              "set_name": "Ultimate Masters",
              "set_uri": "https://api.scryfall.com/sets/2ec77b94-6d47-4891-a480-5d0b4e5c9372",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Auma&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/uma?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A2aa0e0e5-cb6d-4518-8eff-d29f935486e0&unique=prints",
              "collector_number": "175",
              "digital": False,
              "rarity": "rare",
              "illustration_id": "f1677113-e1ad-440c-9ca2-c15ba83e609a",
              "artist": "Greg Staples",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": False,
              "timeshifted": False,
              "colorshifted": False,
              "futureshifted": False,
              "story_spotlight": False,
              "edhrec_rank": 11876,
              "usd": "1.19",
              "tix": "0.26",
              "related_uris": {
                "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=456771",
                "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Nourishing+Shoal&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "edhrec": "http://edhrec.com/route/?cc=Nourishing+Shoal",
                "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Nourishing+Shoal"
              },
              "purchase_uris": {
                "tcgplayer": "https://shop.tcgplayer.com/magic/ultimate-masters/nourishing-shoal?partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "cardmarket": "https://www.cardmarket.com/en/Magic?mainPage=showSearchResult&referrer=scryfall&searchFor=Nourishing+Shoal",
                "cardhoarder": "https://www.cardhoarder.com/cards/70423?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
              }
            },
            {
              "object": "card",
              "id": "ab0d006b-d783-4f63-a3e0-64df98a8b0db",
              "oracle_id": "2aa0e0e5-cb6d-4518-8eff-d29f935486e0",
              "multiverse_ids": [
                457025
              ],
              "name": "Nourishing Shoal",
              "printed_name": "滋養の群れ",
              "lang": "ja",
              "released_at": "2018-12-07",
              "uri": "https://api.scryfall.com/cards/ab0d006b-d783-4f63-a3e0-64df98a8b0db",
              "scryfall_uri": "https://scryfall.com/card/uma/175/ja/%E6%BB%8B%E9%A4%8A%E3%81%AE%E7%BE%A4%E3%82%8C?utm_source=api",
              "layout": "normal",
              "highres_image": False,
              "image_uris": {
                "small": "https://img.scryfall.com/cards/small/front/a/b/ab0d006b-d783-4f63-a3e0-64df98a8b0db.jpg?1544049723",
                "normal": "https://img.scryfall.com/cards/normal/front/a/b/ab0d006b-d783-4f63-a3e0-64df98a8b0db.jpg?1544049723",
                "large": "https://img.scryfall.com/cards/large/front/a/b/ab0d006b-d783-4f63-a3e0-64df98a8b0db.jpg?1544049723",
                "png": "https://img.scryfall.com/cards/png/front/a/b/ab0d006b-d783-4f63-a3e0-64df98a8b0db.png?1544049723",
                "art_crop": "https://img.scryfall.com/cards/art_crop/front/a/b/ab0d006b-d783-4f63-a3e0-64df98a8b0db.jpg?1544049723",
                "border_crop": "https://img.scryfall.com/cards/border_crop/front/a/b/ab0d006b-d783-4f63-a3e0-64df98a8b0db.jpg?1544049723"
              },
              "mana_cost": "{X}{G}{G}",
              "cmc": 2,
              "type_line": "Instant — Arcane",
              "printed_type_line": "インスタント — 秘儀",
              "oracle_text": "You may exile a green card with converted mana cost X from your hand rather than pay this spell's mana cost.\nYou gain X life.",
              "printed_text": "あなたはこの呪文のマナ・コストを支払うのではなく、あなたの手札から点数で見たマナ・コストがＸの緑のカード１枚を追放してもよい。\nあなたはＸ点のライフを得る。",
              "colors": [
                "G"
              ],
              "color_identity": [
                "G"
              ],
              "legalities": {
                "standard": "not_legal",
                "future": "not_legal",
                "frontier": "not_legal",
                "modern": "legal",
                "legacy": "legal",
                "pauper": "not_legal",
                "vintage": "legal",
                "penny": "not_legal",
                "commander": "legal",
                "1v1": "legal",
                "duel": "legal",
                "brawl": "not_legal"
              },
              "games": [
                "mtgo",
                "paper"
              ],
              "reserved": False,
              "foil": True,
              "nonfoil": True,
              "oversized": False,
              "promo": False,
              "reprint": True,
              "set": "uma",
              "set_name": "Ultimate Masters",
              "set_uri": "https://api.scryfall.com/sets/2ec77b94-6d47-4891-a480-5d0b4e5c9372",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Auma&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/uma?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/ab0d006b-d783-4f63-a3e0-64df98a8b0db/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A2aa0e0e5-cb6d-4518-8eff-d29f935486e0&unique=prints",
              "collector_number": "175",
              "digital": False,
              "rarity": "rare",
              "illustration_id": "f1677113-e1ad-440c-9ca2-c15ba83e609a",
              "artist": "Greg Staples",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": False,
              "timeshifted": False,
              "colorshifted": False,
              "futureshifted": False,
              "story_spotlight": False,
              "edhrec_rank": 11876,
              "related_uris": {
                "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=457025&printed=True",
                "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Nourishing+Shoal&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "edhrec": "http://edhrec.com/route/?cc=Nourishing+Shoal",
                "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Nourishing+Shoal"
              },
              "purchase_uris": {
                "tcgplayer": "https://shop.tcgplayer.com/productcatalog/product/show?ProductName=Nourishing+Shoal&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "cardmarket": "https://www.cardmarket.com/en/Magic?mainPage=showSearchResult&referrer=scryfall&searchFor=Nourishing+Shoal",
                "cardhoarder": "https://www.cardhoarder.com/cards?affiliate_id=scryfall&data%5Bsearch%5D=Nourishing+Shoal&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
              }
            },
            {
              "object": "card",
              "id": "ff782973-e33c-4edd-bbd7-5c8dc8d59554",
              "oracle_id": "98aa9424-5912-4bd6-9300-b3972a31d8af",
              "multiverse_ids": [
                456770
              ],
              "mtgo_id": 70029,
              "mtgo_foil_id": 70030,
              "tcgplayer_id": 179490,
              "name": "Noble Hierarch",
              "lang": "en",
              "released_at": "2018-12-07",
              "uri": "https://api.scryfall.com/cards/ff782973-e33c-4edd-bbd7-5c8dc8d59554",
              "scryfall_uri": "https://scryfall.com/card/uma/174/noble-hierarch?utm_source=api",
              "layout": "normal",
              "highres_image": True,
              "image_uris": {
                "small": "https://img.scryfall.com/cards/small/front/f/f/ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg?1545071267",
                "normal": "https://img.scryfall.com/cards/normal/front/f/f/ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg?1545071267",
                "large": "https://img.scryfall.com/cards/large/front/f/f/ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg?1545071267",
                "png": "https://img.scryfall.com/cards/png/front/f/f/ff782973-e33c-4edd-bbd7-5c8dc8d59554.png?1545071267",
                "art_crop": "https://img.scryfall.com/cards/art_crop/front/f/f/ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg?1545071267",
                "border_crop": "https://img.scryfall.com/cards/border_crop/front/f/f/ff782973-e33c-4edd-bbd7-5c8dc8d59554.jpg?1545071267"
              },
              "mana_cost": "{G}",
              "cmc": 1,
              "type_line": "Creature — Human Druid",
              "oracle_text": "Exalted (Whenever a creature you control attacks alone, that creature gets +1/+1 until end of turn.)\n{T}: Add {G}, {W}, or {U}.",
              "power": "0",
              "toughness": "1",
              "colors": [
                "G"
              ],
              "color_identity": [
                "G",
                "U",
                "W"
              ],
              "legalities": {
                "standard": "not_legal",
                "future": "not_legal",
                "frontier": "not_legal",
                "modern": "legal",
                "legacy": "legal",
                "pauper": "not_legal",
                "vintage": "legal",
                "penny": "not_legal",
                "commander": "legal",
                "1v1": "legal",
                "duel": "legal",
                "brawl": "not_legal"
              },
              "games": [
                "mtgo",
                "paper"
              ],
              "reserved": False,
              "foil": True,
              "nonfoil": True,
              "oversized": False,
              "promo": False,
              "reprint": True,
              "set": "uma",
              "set_name": "Ultimate Masters",
              "set_uri": "https://api.scryfall.com/sets/2ec77b94-6d47-4891-a480-5d0b4e5c9372",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Auma&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/uma?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/ff782973-e33c-4edd-bbd7-5c8dc8d59554/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A98aa9424-5912-4bd6-9300-b3972a31d8af&unique=prints",
              "collector_number": "174",
              "digital": False,
              "rarity": "rare",
              "flavor_text": "She protects the sacred groves from blight, drought, and the Unbeholden.",
              "illustration_id": "0a2b9149-9ff1-4097-8377-f3db60ef7ba8",
              "artist": "Mark Zug",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": False,
              "timeshifted": False,
              "colorshifted": False,
              "futureshifted": False,
              "story_spotlight": False,
              "edhrec_rank": 2399,
              "usd": "46.26",
              "eur": "37.88",
              "related_uris": {
                "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=456770",
                "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Noble+Hierarch&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "edhrec": "http://edhrec.com/route/?cc=Noble+Hierarch",
                "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Noble+Hierarch"
              },
              "purchase_uris": {
                "tcgplayer": "https://shop.tcgplayer.com/magic/ultimate-masters/noble-hierarch?partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "cardmarket": "https://www.cardmarket.com/en/Magic/Products/Singles/Ultimate-Masters/Noble-Hierarch?referrer=scryfall",
                "cardhoarder": "https://www.cardhoarder.com/cards/70029?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
              }
            },
            {
              "object": "card",
              "id": "0900e494-962d-48c6-8e78-66a489be4bb2",
              "oracle_id": "7cb29569-48e1-4782-9906-fad155ebfafe",
              "multiverse_ids": [
                414428
              ],
              "mtgo_id": 61220,
              "tcgplayer_id": 119682,
              "name": "Hanweir Garrison",
              "lang": "en",
              "released_at": "2016-07-22",
              "uri": "https://api.scryfall.com/cards/0900e494-962d-48c6-8e78-66a489be4bb2",
              "scryfall_uri": "https://scryfall.com/card/emn/130a/hanweir-garrison?utm_source=api",
              "layout": "meld",
              "highres_image": True,
              "image_uris": {
                "small": "https://img.scryfall.com/cards/small/en/emn/130a.jpg?1526595227",
                "normal": "https://img.scryfall.com/cards/normal/en/emn/130a.jpg?1526595227",
                "large": "https://img.scryfall.com/cards/large/en/emn/130a.jpg?1526595227",
                "png": "https://img.scryfall.com/cards/png/en/emn/130a.png?1526595227",
                "art_crop": "https://img.scryfall.com/cards/art_crop/en/emn/130a.jpg?1526595227",
                "border_crop": "https://img.scryfall.com/cards/border_crop/en/emn/130a.jpg?1526595227"
              },
              "mana_cost": "{2}{R}",
              "cmc": 3.0,
              "type_line": "Creature — Human Soldier",
              "oracle_text": "Whenever Hanweir Garrison attacks, create two 1/1 red Human creature tokens that are tapped and attacking.\n(Melds with Hanweir Battlements.)",
              "power": "2",
              "toughness": "3",
              "colors": [
                "R"
              ],
              "color_identity": [
                "R"
              ],
              "all_parts": [
                {
                  "object": "related_card",
                  "id": "0900e494-962d-48c6-8e78-66a489be4bb2",
                  "component": "meld_part",
                  "name": "Hanweir Garrison",
                  "type_line": "Creature — Human Soldier",
                  "uri": "https://api.scryfall.com/cards/0900e494-962d-48c6-8e78-66a489be4bb2"
                },
                {
                  "object": "related_card",
                  "id": "671fe14d-0070-4bc7-8983-707b570f4492",
                  "component": "meld_result",
                  "name": "Hanweir, the Writhing Township",
                  "type_line": "Legendary Creature — Eldrazi Ooze",
                  "uri": "https://api.scryfall.com/cards/671fe14d-0070-4bc7-8983-707b570f4492"
                },
                {
                  "object": "related_card",
                  "id": "1d743ad6-6ca2-409a-9773-581cc195dbf2",
                  "component": "meld_part",
                  "name": "Hanweir Battlements",
                  "type_line": "Land",
                  "uri": "https://api.scryfall.com/cards/1d743ad6-6ca2-409a-9773-581cc195dbf2"
                },
                {
                  "object": "related_card",
                  "id": "dbd994fc-f3f0-4c81-86bd-14ca63ec229b",
                  "component": "token",
                  "name": "Human",
                  "type_line": "Token Creature — Human",
                  "uri": "https://api.scryfall.com/cards/dbd994fc-f3f0-4c81-86bd-14ca63ec229b"
                }
              ],
              "legalities": {
                "standard": "not_legal",
                "future": "not_legal",
                "frontier": "legal",
                "modern": "legal",
                "legacy": "legal",
                "pauper": "not_legal",
                "vintage": "legal",
                "penny": "not_legal",
                "commander": "legal",
                "1v1": "legal",
                "duel": "legal",
                "brawl": "not_legal"
              },
              "games": [
                "mtgo",
                "paper"
              ],
              "reserved": False,
              "foil": True,
              "nonfoil": True,
              "oversized": False,
              "promo": False,
              "reprint": False,
              "set": "emn",
              "set_name": "Eldritch Moon",
              "set_uri": "https://api.scryfall.com/sets/5f0e4093-334f-4439-bbb5-a0affafd0ffc",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aemn&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/emn?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/0900e494-962d-48c6-8e78-66a489be4bb2/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A7cb29569-48e1-4782-9906-fad155ebfafe&unique=prints",
              "collector_number": "130a",
              "digital": False,
              "rarity": "rare",
              "flavor_text": "\"We're ready for anything!\"",
              "illustration_id": "2b2d858a-8c54-413a-a107-cfc587540ac9",
              "artist": "Vincent Proce",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": False,
              "story_spotlight": False,
              "edhrec_rank": 946,
              "usd": "1.29",
              "tix": "0.01",
              "related_uris": {
                "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=414428",
                "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Hanweir+Garrison&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "edhrec": "http://edhrec.com/route/?cc=Hanweir+Garrison",
                "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Hanweir+Garrison"
              },
              "purchase_uris": {
                "tcgplayer": "https://shop.tcgplayer.com/magic/eldritch-moon/hanweir-garrison?partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
                "cardmarket": "https://www.cardmarket.com/en/Magic?mainPage=showSearchResult&referrer=scryfall&searchFor=Hanweir+Garrison",
                "cardhoarder": "https://www.cardhoarder.com/cards/61220?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
              }
            }
        ]
        self.assertTrue(validator.iscardlist(d))
    
    
    # Tests for validator.isdataresp().
    def test_isdataresp(self):
        """Unit tests for validator.isdataresp()."""
        ctype = {'mediatype': 'application/json',
                 'charset': 'utf-8',}
        self.assertTrue(validator.isdataresp(ctype))

    def test_isdataresp_CtypeIsList(self):
        """DTest is ctype is wrong type."""
        ctype = ['application/json',
                 'utf-8',]
        name = 'data response'
        regex = "{} value must be of type {}.".format(name, dict)
        self.assertRaisesRegex(TypeError, regex, validator.isdataresp, ctype)

    def test_isdataresp_NoCharset(self):
        """Test if missing charset."""
        ctype = {'mediatype': 'application/json',}
        name = 'data response'
        regex = "{} has invalid value.".format(name)
        self.assertRaisesRegex(ValueError, regex, validator.isdataresp, ctype)

    def test_isdataresp_IsHTML(self):
        """Test if mediatype is wrong."""
        ctype = {'mediatype': 'text/html',
                 'charset': 'utf-8',}
        name = 'mediatype'
        regex = "{} has invalid value.".format(name)
        self.assertRaisesRegex(ValueError, regex, validator.isdataresp, ctype)

    def test_isdataresp_CharsetaIsUTF16(self):
        """Test if charset is invalid."""
        ctype = {'mediatype': 'application/json',
                 'charset': 'utf-16',}
        name = 'charset'
        regex = "{} has invalid value.".format(name)
        self.assertRaisesRegex(ValueError, regex, validator.isdataresp, ctype)


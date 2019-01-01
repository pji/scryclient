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
from scrycli import scrycli, validator

# Global configuration settings.
FQDN = None
SCRYFAKE_FQDN = 'http://127.0.0.1:5000'

# Common exception messages.
badtype = '{} value must be of type {}.'
badvalue = '{} has invalid value.'


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
    
    def test_sets(self):
        """Unit test for the scrycli.sets."""
        #expected = ('application/json; charset=utf-8', scryfake.resp['sets'])
        resp = scryfake.resp['sets']
        expected = loads(resp)['data']
        self.assertEqual(scrycli.sets(), expected)
    
    
    def test_sets_validator(self):
        """Positive test for scrycli.sets_validator()."""
        resp = scryfake.resp['sets']
        ctype = 'application/json; charset=utf-8'
        expected = loads(resp)['data']
        self.assertEqual(scrycli.sets_validator(ctype, resp), expected)
    
    
    def test_sets_validator_CtypeIsList(self):
        """Unit test for scrycli.sets_validator."""
        ctype = [1, 2]
        content = b'foo'
        regex = "ctype must be a str. Was: <class 'list'>"
        self.assertRaisesRegex(TypeError, regex, scrycli.sets_validator,
                               ctype, content)
    
    def test_sets_validator_NoCset(self):
        ctype = 'text/html'
        content = b'foo'
        regex = 'Content-Type must have structure: .* set>'
        self.assertRaisesRegex(ValueError, regex, scrycli.sets_validator,
                               ctype, content)
    
    def test_sets_validator_MtypeIsHTML(self):
        ctype = 'text/html; charset=utf-8'
        content = b'foo'
        regex = 'Content-Type must be application/json.'
        self.assertRaisesRegex(ValueError, regex, scrycli.sets_validator,
                               ctype, content)
    
    def test_sets_validator_CsetIsUTF16(self):
        ctype = 'application/json; charset=utf-16'
        content = b'foo'
        regex = 'Character set must be utf-8.'
        self.assertRaisesRegex(ValueError, regex, scrycli.sets_validator,
                               ctype, content)
    
    def test_sets_validator_ContentIsList(self):
        ctype = 'application/json; charset=utf-8'
        content = [1, 2]
        regex = 'content must be bytes.'
        self.assertRaisesRegex(TypeError, regex, scrycli.sets_validator,
                               ctype, content)
    
    def test_sets_validator_ContentBadCharacter(self):
        """Ensure exception thrown if invalid UTF-8 sequence 
        is present.
        """
        ctype = 'application/json; charset=utf-8'
        content = b'Montr\xe9al'
        regex = 'content must be valid utf-8.'
        self.assertRaisesRegex(ValueError, regex, scrycli.sets_validator,
                               ctype, content)
    
    def test_sets_validator_ContentNotJSON(self):
        """Ensure exception thrown if content isn't JSON."""
        ctype = 'application/json; charset=utf-8'
        content = b'{foo]'
        regex = 'content must be valid JSON.'
        self.assertRaisesRegex(ValueError, regex, scrycli.sets_validator,
                               ctype, content)
        
    def test_sets_validator_ContentNoDataKey(self):
        """Ensure exception thrown if content isn't JSON."""
        ctype = 'application/json; charset=utf-8'
        content = b'{"object": "list", "has_more": false}'
        regex = 'content must have a key named data.'
        self.assertRaisesRegex(ValueError, regex, scrycli.sets_validator,
                               ctype, content)
        
    def test_sets_validator_ContentDataNotList(self):
        """Ensure exception thrown if content isn't JSON."""
        ctype = 'application/json; charset=utf-8'
        content = b'{"object": "list", "has_more": false, "data": "hi"}'
        regex = 'Sets must be in a list.'
        self.assertRaisesRegex(ValueError, regex, scrycli.sets_validator,
                               ctype, content)
        
    @classmethod
    def tearDownClass(cls):
        """Tear down test instances and data."""
        # Shutdown the Scryfake instance.
        get('http://127.0.0.1:5000/shutdown')
        
        # Point scrycli back at Scryfall.com just in case.
        global FQDN
        scrycli.FQDN = FQDN
        FQDN = None


class ValidatorTestCase(unittest.TestCase):
    """Unit tests for validator."""
    def test_isobject(self):
        """Tests for isobject(s)."""
        s = 'set'
        self.assertTrue(validator.isobject(s))
        
        # Not a string.
        s = [1, 2]
        regex = badtype.format('object', str)
        self.assertRaisesRegex(TypeError, regex, validator.isobject, s)
        
        # Not a valid object.
        s = 'spam'
        regex = badvalue.format('object')
        self.assertRaisesRegex(ValueError, regex, validator.isobject, s)
    
    
    def test_isid(self):
        """Tests for isid(s)."""
        s = 'a4a0db50-8826-4e73-833c-3fd934375f96'
        self.assertTrue(validator.isid(s))
    
        # Not a string.
        s = [1, 2]
        regex = badtype.format('id', str)
        self.assertRaisesRegex(TypeError, regex, validator.isid, s)
        
        # Not a UUID.
        s = '12345'
        regex = badvalue.format('id')
        self.assertRaisesRegex(ValueError, regex, validator.isid, s)
    
    
    def test_iscode(self):
        """Tests for issetcode(s)."""
        s = 'aer'
        self.assertTrue(validator.iscode(s))
    
        # Not a string.
        s = [1, 2]
        regex = badtype.format('code', str)
        self.assertRaisesRegex(TypeError, regex, validator.iscode, s)
        
        # Too short.
        s = 'a'
        regex = badvalue.format('code')
        self.assertRaisesRegex(ValueError, regex, validator.iscode, s)
        
        # Too long.
        s = 'aerK+J3'
        regex = badvalue.format('code')
        self.assertRaisesRegex(ValueError, regex, validator.iscode, s)
    
    
    def test_istcgplayer_id(self):
        """Positive test for istcgplayer_id(s)."""
        n = 123
        self.assertTrue(validator.istcgplayer_id(n))
        
        # Not an integer.
        n = [1, 2]
        regex = badtype.format('tcgplayer_id', int)
        self.assertRaisesRegex(TypeError, regex, validator.istcgplayer_id, n)
    
    
    def test_isname(self):
        """Positive test for isname(s)."""
        s = 'Aether Revolt'
        self.assertTrue(validator.isname(s))
        
        # Not a string.
        s = [1, 2]
        regex = badtype.format('name', str)
        self.assertRaisesRegex(TypeError, regex, validator.isname, s)
    
    
    def test_isset_type(self):
        """Positive test for isset_type(s)."""
        s = 'core'
        self.assertTrue(validator.isset_type(s))
        
        # Not a str.
        s = [1, 2]
        regex = badtype.format('set_type', str)
        self.assertRaisesRegex(TypeError, regex, validator.isset_type, s)
        
        # Not a valid type.
        s = '12345'
        regex = badvalue.format('set_type')
        self.assertRaisesRegex(ValueError, regex, validator.isset_type, s)
    
    
    def test_isdate(self):
        """Positive test for isdate(s)."""
        s = '2017-01-20'
        self.assertTrue(validator.isdate(s))
        
        # Not a str.
        s = [1, 2]
        regex = badtype.format('date', str)
        self.assertRaisesRegex(TypeError, regex, validator.isdate, s)
        
        # Not a valid date.
        s = '12345'
        regex = badvalue.format('date')
        self.assertRaisesRegex(ValueError, regex, validator.isdate, s)
    
    
    def test_iscard_count(self):
        """Test for iscard_count(s)."""
        n = 278
        self.assertTrue(validator.iscard_count(n))
        
        # Not a str.
        n = [1, 2]
        regex = badtype.format('card_count', int)
        self.assertRaisesRegex(TypeError, regex, validator.iscard_count, n)
    
    
    def test_isbool(self):
        """Tests for isbool(s)."""
        b = False
        self.assertTrue(validator.isbool(b))
        
        # Not a str.
        b = [1, 2]
        regex = badtype.format('boolean', bool)
        self.assertRaisesRegex(TypeError, regex, validator.isbool, b)
    
    
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
    
    
    def test_isapiurl(self):
        """Tests for isapiurl(s)."""
        s = 'https://api.scryfall.com/sets'
        self.assertTrue(validator.isapiurl(s))
        
        # Not a valid netloc
        s = 'https://test.test'
        regex = badvalue.format('api_url')
        self.assertRaisesRegex(ValueError, regex, validator.isapiurl, s)
    
    
    def test_isimgurl(self):
        """Tests for isimgurl(s)."""
        s = 'https://img.scryfall.com/sets'
        self.assertTrue(validator.isimgurl(s))
        
        # Not a valid netloc
        s = 'https://test.test'
        regex = badvalue.format('img_url')
        self.assertRaisesRegex(ValueError, regex, validator.isimgurl, s)
    
    
    def test_iscryfallurl(self):
        """Tests for isimgurl(s)."""
        s = 'https://scryfall.com/sets'
        self.assertTrue(validator.isscryfallurl(s))
        
        # Not a valid netloc
        s = 'https://test.test'
        regex = badvalue.format('scryfall_url')
        self.assertRaisesRegex(ValueError, regex, validator.isscryfallurl, s)
    
    
    def test_issetobject(self):
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
        self.assertTrue(validator.issetobject(d))

    
    

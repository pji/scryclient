# -*- coding: utf-8 -*-
"""
tests
~~~~~

Implements the unit tests for the scrycli module.

Run from module root with:
python3 -m unittest tests/tests.py
"""

from collections.abc import Mapping, Sequence
from json import loads
from threading import Thread
from time import sleep
import unittest

from requests import get

from tests import scryfake
from scrycli import scrycli, utility
from scrycli.pyvalidate import pyvalidate as PV
from scrycli.pyvalidate import normalize as N


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
    
    
    # Tests for sets().
    def test_sets(self):
        """Unit test for the scrycli.sets."""
        #expected = ('application/json; charset=utf-8', scryfake.resp['sets'])
        resp = scryfake.resp['sets']
        expected = loads(resp)
        self.assertEqual(scrycli.sets(), expected)
    
    
    # Tests for sets_code().
    def test_set_code_Happy(self):
        """scrycli.sets_code() positive case."""
        code = 'mmq'
        pretty = True
        resp = scryfake.resp['sets_code']
        expected = loads(resp)
        self.assertEqual(scrycli.sets_code(code, pretty), expected)
    
    
    # Tests for cards().
    def test_cards(self):
        """Unit tests for cards()."""
        resp = scryfake.resp['cards']
        expected = loads(resp)
        self.assertEqual(scrycli.cards(), expected)

    
    # Tests for cards_search().
    def test_cards_search(self):
        """Unit tests for cardsearch()."""
        q = 's:ktk'
        resp = scryfake.resp['cards_search']
        expected = loads(resp, strict=False)
        self.assertEqual(scrycli.cards_search(q), expected)


    # Tests for _get().
    def test_get_404(self):
        """scrycli._get() negative case: return code 404."""
        code='zzz'
        resp = scryfake.resp['sets_code']
        err = scrycli.HTTPClientError
        msg = '404: NOT FOUND'
        self.assertRaisesRegex(err, msg, scrycli.sets_code, code)
        
    
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
    # Tests for build_query().
    def test_build_query(self):
        """Unit test for utility.build_query()."""
        kwargs = {'cardset': 'rna'}
        expected = 'set:rna '
        self.assertEqual(utility.build_query(**kwargs), expected)
    
    
    # Tests for parse_manacost().
    def test_parse_manacost(self):
        """Unit tests for utility.parse_manacost(s)."""
        s = '{2}{W}{U}'
        expected = ['{2}', '{W}', '{U}']
        self.assertEqual(utility.parse_manacost(s), expected)


class PVTestCase(unittest.TestCase):
    """Unit tests for pyvalidate.pyvalidate."""
    # Tests for isvalid().
    def test_isvalid_HappyInt(self):
        """PV.isvalid() positive test: integer validation."""
        item = 44
        name = 'Integer'
        vtype = (int, float)
        min = 0
        max = 100
        self.assertTrue(PV.isvalid(item, name, vtype, 
                                           min=min, max=max))

    def test_isvalid_BadType(self):
        """PV.isvalid() negative test: type validation."""
        item = 44
        name = 'Integer'
        vtype = str
        min = 0
        max = 100
        err = TypeError
        msg_re = '{} must be of type {}. Was {}.'.format(name, str, int)
        self.assertRaisesRegex(err, msg_re, PV.isvalid, item, name, 
                               vtype, min=min, max=max)
        
    def test_isvalid_MaxInt(self):
        """PV.isvalid() negative test: integer maximum."""
        item = 103
        name = 'Integer'
        vtype = (int, float)
        min = 0
        max = 100
        err = ValueError
        msg_re = '{} cannot be more than {}.'.format(name, max)
        self.assertRaisesRegex(err, msg_re, PV.isvalid, item, name, 
                               vtype, min=min, max=max)
    
    def test_isvalid_MinInt(self):
        """PV.isvalid() negative test: integer minimum."""
        item = 0
        name = 'Integer'
        vtype = (int, float)
        min = 10
        max = 100
        err = ValueError
        msg_re = '{} must be at least {}.'.format(name, min)
        self.assertRaisesRegex(err, msg_re, PV.isvalid, item, name, 
                               vtype, min=min, max=max)
    
    def test_isvalid_Minlen(self):
        """PV.isvalid() negative test: string min length."""
        item = 'spam'
        name = 'String'
        vtype = str
        minlen = 10
        maxlen = 100
        err = ValueError
        msg_re = '{} must be longer than {}.'.format(name, minlen)
        self.assertRaisesRegex(err, msg_re, PV.isvalid, item, name, 
                               vtype, minlen=minlen, maxlen=maxlen)
    
    def test_isvalid_Maxlen(self):
        """PV.isvalid() negative test: string max length."""
        item = 'spam'
        name = 'String'
        vtype = str
        minlen = 1
        maxlen = 3
        err = ValueError
        msg_re = '{} must be shorter than {}.'.format(name, maxlen)
        self.assertRaisesRegex(err, msg_re, PV.isvalid, item, name, 
                               vtype, minlen=minlen, maxlen=maxlen)
    
    def test_isvalid_Pattern(self):
        """PV.isvalid() negative test: string pattern."""
        item = 'spam'
        name = 'String'
        vtype = str
        pattern = '^e.*s$'
        err = ValueError
        msg_re = '{} must match pattern .*\.'.format(name)
        self.assertRaisesRegex(err, msg_re, PV.isvalid, item, name, 
                               vtype, pattern=pattern)
    
    
    # Tests for isvalidseq().
    def test_isvalidseq_HappyTuple(self):
        """PV.isvalidseq positive test: tuple."""
        item = ('spam', 'eggs', 'sausage', 'baked beans', 'spam')
        name = 'Spam Sketch'
        val = PV.isvalid
        valkwargs = {
            'validtype': str,
            'enum': [
                'spam',
                'eggs',
                'sausage',
                'baked beans',
            ],
        }
        self.assertTrue(PV.isvalidseq(item, name, val, valkwargs))
    
    def test_isvalidseq_HappyStr(self):
        """PV.isvalidseq positive test: str."""
        item = 'spam'
        name = 'Spam Sketch'
        val = PV.isvalid
        valkwargs = {
            'validtype': str,
            'enum': [
                's',
                'p',
                'a',
                'm',
            ],
        }
        self.assertTrue(PV.isvalidseq(item, name, val, valkwargs))
    
    def test_isvalidseq_BadMember(self):
        """PV.isvalidseq negative test: invalid member."""
        item = ('spam', 'eggs', 'sausage', 'baked beans', 'spam')
        name = 'Spam Sketch'
        val = PV.isvalid
        valkwargs = {
            'validtype': str,
            'enum': [
                'spam',
                'eggs',
                'baked beans',
            ],
        }
        args = [item, name, val, valkwargs]
        err = ValueError
        msg_re = 'Spam Sketch:2 does not match a value in list.'
        self.assertRaisesRegex(err, msg_re, PV.isvalidseq, *args)
    
    def test_isvalidseq_Nesting(self):
        """PV.isvsalidseq positive test: list nesting."""
        item = [
            (['0', '5'], ['x', 'y']),
            (['2', '4'], ['x', 'y']),
            (['1', '1'], ['x', 'y']),
            (['3', '3'], ['x', 'y']),
            (['4', '1'], ['x', 'y']),
        ]
        name = 'Coords'
        val = PV.isvalidseq
        valkwargs = {
            'val': PV.isvalidseq,
            'valkwargs': {
                'val': PV.isvalid,
                'valkwargs': {
                    'validtype': str,
                    'pattern': '^[xy0-5]$',
                },
            },
        }
        args = [item, name, val, valkwargs]
        self.assertTrue(PV.isvalidseq(*args))
    
    
    # Tests for isvalidmap().
    def test_isvalidmap_Happy(self):
        """PV.isvalidmap() positive test."""
        d = {
            'name': 'Terry Jones',
            'type': 'animal',
            'score': 98,
        }
        name = 'Python'
        req = {
            'name': {
                'val': PV.isvalid,
                'valkwargs': {
                    'validtype': str,
                },
            },
            'type': {
                'val': PV.isvalid,
                'valkwargs': {
                    'validtype': str,
                    'enum': [
                        'animal',
                        'vegetable',
                        'mineral',
                    ],
                },
            },
        }
        opt = {
            'score': {
                'val': PV.isvalid,
                'valkwargs': {
                    'validtype': int,
                    'min': 0,
                    'max': 100,
                },
            },
        }
        args = (d, name, req, opt)
        self.assertTrue(PV.isvalidmap(*args))
    
    def test_isvalidmap_Nesting(self):
        """PV.isvalidmap() positive test: nesting"""
        d = {
            'name': 'Michael Palin',
            'type': 'animal',
            'score': [98, 95, 99],
            'pet': {
                'name': 'Wanda',
                'type': 'animal',
                'subtype': 'fish',
            },
        }
        name = 'Python'
        req = {
            'name': {
                'val': PV.isvalid,
                'valkwargs': {
                    'validtype': str,
                },
            },
            'type': {
                'val': PV.isvalid,
                'valkwargs': {
                    'validtype': str,
                    'enum': [
                        'animal',
                        'vegetable',
                        'mineral',
                    ],
                },
            },
        }
        opt = {
            'score': {
                'val': PV.isvalidseq,
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': {
                        'validtype': int,
                        'min': 0,
                        'max': 100,
                    },
                },
            },
            'pet': {
                'val': PV.isvalidmap,
                'valkwargs': {
                    'req': {
                        'name': {
                            'val': PV.isvalid,
                            'valkwargs': {
                                'validtype': str,
                            },
                        },
                        'type': {
                            'val': PV.isvalid,
                            'valkwargs': {
                                'validtype': str,
                                'enum': [
                                    'animal',
                                    'vegetable',
                                    'mineral',
                                ],
                            },
                        },
                        'subtype': {
                            'val': PV.isvalid,
                            'valkwargs': {
                                'validtype': str,
                                'enum': [
                                    'dog',
                                    'cat',
                                    'ferret',
                                    'skunk',
                                    'fish',     
                                ],
                            },
                        },
                    },
                },
            },
        }
        args = (d, name, req, opt)
        self.assertTrue(PV.isvalidmap(*args))
    
    def test_isvalidmap_BadNest(self):
        """PV.isvalidmap() negative test: nested bad type"""
        d = {
            'name': 'Michael Palin',
            'type': 'animal',
            'score': [98, 95, 99],
            'pet': 'Wanda',
        }
        name = 'Python'
        req = {
            'name': {
                'val': PV.isvalid,
                'valkwargs': {
                    'validtype': str,
                },
            },
            'type': {
                'val': PV.isvalid,
                'valkwargs': {
                    'validtype': str,
                    'enum': [
                        'animal',
                        'vegetable',
                        'mineral',
                    ],
                },
            },
        }
        opt = {
            'score': {
                'val': PV.isvalidseq,
                'valkwargs': {
                    'val': PV.isvalid,
                    'valkwargs': {
                        'validtype': int,
                        'min': 0,
                        'max': 100,
                    },
                },
            },
            'pet': {
                'val': PV.isvalidmap,
                'valkwargs': {
                    'req': {
                        'name': {
                            'val': PV.isvalid,
                            'valkwargs': {
                                'validtype': str,
                            },
                        },
                        'type': {
                            'val': PV.isvalid,
                            'valkwargs': {
                                'validtype': str,
                                'enum': [
                                    'animal',
                                    'vegetable',
                                    'mineral',
                                ],
                            },
                        },
                        'subtype': {
                            'val': PV.isvalid,
                            'valkwargs': {
                                'validtype': str,
                                'enum': [
                                    'dog',
                                    'cat',
                                    'ferret',
                                    'skunk',
                                    'fish',     
                                ],
                            },
                        },
                    },
                },
            },
        }
        args = (d, name, req, opt)
        err = TypeError
        msg_re = 'Python:pet must be of type {}. Was {}'.format(Mapping, str)
        self.assertRaisesRegex(err, msg_re, PV.isvalidmap, *args)
    
    
    # Tests for isvalidurl().
    def test_isvalidurl_Happy(self):
        """PV.isvalidurl() positive test."""
        s = 'https://www.test.test/test.html?q=test#main'
        name = 'URL'
        kwargs = {
            'vscheme': 'https',
            'vnetloc': 'www.test.test',
            'vpath': '/test.html',
            'vquery': 'q=test',
            'vfrag': 'main',
        }
        self.assertTrue(PV.isvalidurl(s, name, **kwargs))
    
    def test_isvalidurl_BadType(self):
        """PV.isvalidurl() positive test."""
        s = [1, 2, 3]
        name = 'URL'
        kwargs = {
            'vscheme': 'https',
            'vnetloc': 'www.test.test',
            'vpath': '/test.html',
            'vquery': 'q=test',
            'vfrag': 'main',
        }
        err = TypeError
        msg_re = 'URL must be of type {}. Was {}.'.format(str, list)
        self.assertRaisesRegex(err, msg_re, PV.isvalidurl, s, name, **kwargs)
    
    def test_isvalidurl_BadScheme(self):
        """PV.isvalidurl() positive test."""
        s = 'http://www.test.test/test.html?q=test#main'
        name = 'URL'
        kwargs = {
            'vscheme': 'https',
            'vnetloc': 'www.test.test',
            'vpath': '/test.html',
            'vquery': 'q=test',
            'vfrag': 'main',
        }
        err = ValueError
        msg_re = 'URL:scheme has invalid value\.'
        self.assertRaisesRegex(err, msg_re, PV.isvalidurl, s, name, **kwargs)
    
    def test_isvalidurl_BadNetloc(self):
        """PV.isvalidurl() positive test."""
        s = 'https://www2.test.test/test.html?q=test#main'
        name = 'URL'
        kwargs = {
            'vscheme': 'https',
            'vnetloc': 'www.test.test',
            'vpath': '/test.html',
            'vquery': 'q=test',
            'vfrag': 'main',
        }
        err = ValueError
        msg_re = 'URL:netloc has invalid value\.'
        self.assertRaisesRegex(err, msg_re, PV.isvalidurl, s, name, **kwargs)
    
    def test_isvalidurl_BadPath(self):
        """PV.isvalidurl() positive test."""
        s = 'https://www.test.test/test2.html?q=test#main'
        name = 'URL'
        kwargs = {
            'vscheme': 'https',
            'vnetloc': 'www.test.test',
            'vpath': '/test.html',
            'vquery': 'q=test',
            'vfrag': 'main',
        }
        err = ValueError
        msg_re = 'URL:path has invalid value\.'
        self.assertRaisesRegex(err, msg_re, PV.isvalidurl, s, name, **kwargs)
    
    
    # Tests for validate_httpjson().
    def test_validate_httpjson_Happy(self):
        """PV.validate_httpjson positive test."""
        ctype = 'application/json; charset=utf-8'
        content = """{
            "name": "Terry Jones",
            "type": "animal",
            "score": 98
        }"""
        name = 'Test HTTPJSON'
        val = PV.isvalidmap
        valkwargs = {
            'req': {
                'name': {
                    'val': PV.isvalid,
                    'valkwargs': {
                        'validtype': str,
                    }
                },
                'type': {
                    'val': PV.isvalid,
                    'valkwargs': {
                        'validtype': str,
                        'enum': [
                            'animal',
                            'mineral',
                            'vegetable',
                        ],
                    }
                },
                'score': {
                    'val': PV.isvalid,
                    'valkwargs': {
                        'validtype': int,
                        'min': 50,
                        'max': 100
                    }
                }
            }
        }
        result = PV.validate_httpjson(ctype, content, name, val, valkwargs)
        expected = {
            "name": "Terry Jones",
            "type": "animal",
            "score": 98
        }
        self.assertEqual(result, expected)


class NormalizeTestCase(unittest.TestCase):
    """Test cases for pyvalidate.normalize."""
    # Tests for canonicalize().
    def test_canonicalize_Happy(self):
        """Happy path bytes test for canonicalize()."""
        text = b'Montr\xc3\xa9al'
        expected = 'Montréal'
        self.assertEqual(N.canonicalize(text), expected)
        
    def test_canonicalize_HappyStr(self):
        """N.canonicalize() postive test: str input."""
        text = '\u2126'
        expected = '\u03a9'
        self.assertEqual(N.canonicalize(text), expected)

    def test_canonicalize_BadCharacter(self): 
        text = b'Montr\xe9al'
        name = 'city'
        vtype = bytes
        encoding = 'utf_8'
        ex = ValueError
        pattern = 'Text was not valid {}[.]'.format(encoding)
        self.assertRaisesRegex(ex, pattern, N.canonicalize, 
                               text, dest_encoding=encoding)

    def test_canonicalize_BadForm(self): 
        text = b'Montr\xc3\xa9al'
        name = 'city'
        vtype = bytes
        encoding = 'utf_8'
        form = 'XXX'
        ex = ValueError
        pattern = 'invalid normalization form'
        self.assertRaisesRegex(ex, pattern, N.canonicalize, 
                               text, dest_encoding=encoding, 
                               dest_form=form)
    
    
    # Tests for from_json().
    def test_from_json_Happy(self):
        """N.from_json() positive test."""
        text = """{
            "name": "Terry Jones",
            "type": "animal",
            "score": 98
        }"""
        expected = {
            'name': 'Terry Jones',
            'type': 'animal',
            'score': 98,
        }
        self.assertEqual(N.from_json(text), expected)
    
    def test_from_json_BadJSON(self):
        """N.from_json() negative test: invalid JSON."""
        text = '{]'
        err = TypeError
        msg_re = 'Text was not valid JSON.'
        self.assertRaisesRegex(err, msg_re, N.from_json, text)

    
    # Tests for from_ctype().
    def test_from_ctype_Happy(self):
        """N.from_ctype() positive test."""
        s = 'application/json; charset=utf-8'
        expected = {
            'mediatype': 'application/json',
            'charset': 'utf-8',
        }
        self.assertEqual(N.from_ctype(s), expected)
    
    
    # Tests for normalize().
    def test_normalize_Happy(self):
        """N.normalize() positive test."""
        s = 'application/json; charset=utf-8'
        tf = N.from_ctype
        expected = {
            'mediatype': 'application/json',
            'charset': 'utf-8',
        }
        self.assertEqual(N.normalize(s, tf), expected)


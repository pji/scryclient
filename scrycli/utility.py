# -*- coding: utf-8 -*-
"""
utility
~~~~~~~

General utilities used for scrycli.
"""
def build_query(cardset=None):
    """Build a query for Scryfall.com's full text search.
    
    :param set: (Optional.) The set code to search for.
    :return: A :class:string with the query.
    :rtype: string
    """
    q = ''
    if cardset:
        q += 'set:{} '.format(cardset)
    return q


def parse_manacost(s: str):
    """
    Split a mana cost string into a list of each mana cost symbol 
    in the string.
    
    :param cost: The mana cost :class:string.
    :return: :class:list
    :rtype: list
    """
    cost = s[:]
    out = []
    buf = ''
    
    # Handle split card mana costs
    cost = cost.replace(' // ', '')
    
    for char in cost:
        buf += char
        if char == '}' or char == ' ':
            out.append(buf)
            buf = ''
    return out
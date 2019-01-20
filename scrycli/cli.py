# -*- coding: utf-8 -*-
"""
cli
~~~

A simple command line client for scrycli. This is intended more to 
demonstrate and experiment with than for actual use.
"""
from argparse import ArgumentParser
from operator import itemgetter
from time import sleep
from .scrycli import cards, sets, cards_search
from .utility import build_query

def list_cards():
    """Print a list of MtG cards to stdout."""
    fmt = '{:<40}{:<10}{:<10}'
    cardslist = cards()
    for card in cardslist['data']:
        print(fmt.format(card['name'], card['collector_number'], card['set']))


def list_sets():
    """Print a list of Magic the Gathering (MtG) sets to stdout."""
    fmt = '{:<50}{:<8}'
    setslist = sets()
    sorted_sets = sorted(setslist['data'], key=itemgetter('released_at'))
    for set in sorted_sets:
        print(fmt.format(set['name'], set['code']))


def list_cards_in_set(cardset):
    """Print a list of MtG cards in a given set to stdout."""
    fmt = '{:<40}{:<10}{:<10}'
    q = build_query(cardset=cardset)
    page = 1
    cardslistobj = cards_search(q)
    cards = cardslistobj['data']
    while cardslistobj['has_more']:
        sleep(.25)
        page += 1
        cardslistobj = cards_search(q, page=page)
        cards.extend(cardslistobj['data'])
    for card in cards:
        print(fmt.format(card['name'], card['collector_number'], card['set']))


def _cli():
    """Parse command line arguments and execute the commands."""
    # Set up the command line argument parser.
    parser = ArgumentParser()
    parser.add_argument('-c', '--cards', help='list MtG cards', 
                        action='store_true')
    parser.add_argument('-s', '--sets', help='list MtG sets', 
                        action='store_true')
    parser.add_argument('-C', '--cardsinset', help='list MtG cards in a set',
                        nargs=1, action='store')
    args = parser.parse_args()
    
    # Act on the command line arguments.
    if args.cards:
        list_cards()
    if args.sets:
        list_sets()
    if args.cardsinset:
        list_cards_in_set(args.cardsinset[0])


if __name__ == '__main__':
    _cli()
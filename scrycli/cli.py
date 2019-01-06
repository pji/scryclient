# -*- coding: utf-8 -*-
"""
cli
~~~

A simple command line client for scrycli. This is intended more to 
demonstrate and experiment with than for actual use.
"""
from argparse import ArgumentParser
from operator import itemgetter
from .scrycli import cards, sets

def list_cards():
    """Print a list of MtG cards to stdout."""
    fmt = '{:<30}{:<10}{:<10}'
    cardslist = cards()
    for card in cardslist:
        print(fmt.format(card['name'], card['collector_number'], card['set']))


def list_sets():
    """Print a list of Magic the Gathering (MtG) sets to stdout."""
    fmt = '{:<50}{:<8}'
    setslist = sets()
    sorted_sets = sorted(setslist, key=itemgetter('released_at'))
    for set in sorted_sets:
        print(fmt.format(set['name'], set['code']))


def _cli():
    """Parse command line arguments and execute the commands."""
    # Set up the command line argument parser.
    parser = ArgumentParser()
    parser.add_argument('-c', '--cards', help='list MtG cards', 
                        action='store_true')
    parser.add_argument('-s', '--sets', help='list MtG sets', 
                        action='store_true')
    args = parser.parse_args()
    
    # Act on the command line arguments.
    if args.cards:
        list_cards()
    if args.sets:
        list_sets()


if __name__ == '__main__':
    _cli()
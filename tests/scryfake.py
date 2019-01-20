# -*- coding: utf-8 -*-
"""
scryfake
~~~~~~~~

A dummy version of Scryfall.com for use in unit tests.
"""
from flask import Flask, request

# Create the web application.
app = Flask(__name__)

# The response text is stored here for ease of access in the 
# unit tests.
resp = {
    'sets': b'''{
          "object": "list",
          "has_more": false,
          "data": [
            {
              "object": "set",
              "id": "ee3a8eb6-0583-492b-8be5-265795d38038",
              "code": "prw2",
              "name": "RNA Ravnica Weekend",
              "uri": "https://api.scryfall.com/sets/ee3a8eb6-0583-492b-8be5-265795d38038",
              "scryfall_uri": "https://scryfall.com/sets/prw2",
              "search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aprw2&unique=prints",
              "released_at": "2019-02-16",
              "set_type": "promo",
              "card_count": 10,
              "parent_set_code": "rna",
              "digital": false,
              "foil_only": false,
              "icon_svg_uri": "https://img.scryfall.com/sets/rna.svg?1546232400"
            },
            {
              "object": "set",
              "id": "97a7fd84-8d89-45a3-b48b-c951f6a3f9f1",
              "code": "rna",
              "mtgo_code": "rna",
              "tcgplayer_id": 2366,
              "name": "Ravnica Allegiance",
              "uri": "https://api.scryfall.com/sets/97a7fd84-8d89-45a3-b48b-c951f6a3f9f1",
              "scryfall_uri": "https://scryfall.com/sets/rna",
              "search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Arna&unique=prints",
              "released_at": "2019-01-25",
              "set_type": "expansion",
              "card_count": 21,
              "digital": false,
              "foil_only": false,
              "icon_svg_uri": "https://img.scryfall.com/sets/rna.svg?1546232400"
            },
            {
              "object": "set",
              "id": "7766a0e4-ff37-4ceb-b68c-6f9336c64ba0",
              "code": "trna",
              "name": "Ravnica Allegiance Tokens",
              "uri": "https://api.scryfall.com/sets/7766a0e4-ff37-4ceb-b68c-6f9336c64ba0",
              "scryfall_uri": "https://scryfall.com/sets/trna",
              "search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Atrna&unique=prints",
              "released_at": "2019-01-25",
              "set_type": "token",
              "card_count": 1,
              "parent_set_code": "rna",
              "digital": false,
              "foil_only": false,
              "icon_svg_uri": "https://img.scryfall.com/sets/rna.svg?1546232400"
            },
            {
              "object": "set",
              "id": "503230ec-81e3-4f92-b847-ff435b1652e0",
              "code": "prna",
              "name": "Ravnica Allegiance Promos",
              "uri": "https://api.scryfall.com/sets/503230ec-81e3-4f92-b847-ff435b1652e0",
              "scryfall_uri": "https://scryfall.com/sets/prna",
              "search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aprna&unique=prints",
              "released_at": "2019-01-25",
              "set_type": "promo",
              "card_count": 7,
              "parent_set_code": "rna",
              "digital": false,
              "foil_only": false,
              "icon_svg_uri": "https://img.scryfall.com/sets/rna.svg?1546232400"
            }
          ]
    }''',
    'sets_code': b'''{
        "object": "set",
        "id": "385e11a4-492b-4d07-b4a6-a1409ef829b8",
        "code": "mmq",
        "mtgo_code": "mm",
        "tcgplayer_id": 73,
        "name": "Mercadian Masques",
        "uri": "https://api.scryfall.com/sets/385e11a4-492b-4d07-b4a6-a1409ef829b8",
        "scryfall_uri": "https://scryfall.com/sets/mmq",
        "search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Ammq&unique=prints",
        "released_at": "1999-10-04",
        "set_type": "expansion",
        "card_count": 350,
        "digital": false,
        "foil_only": false,
        "block_code": "mmq",
        "block": "Masques",
        "icon_svg_uri": "https://img.scryfall.com/sets/mmq.svg?1547442000"
    }''',
    'cards': r'''{
        "object": "list",
        "total_cards": 233142,
        "has_more": true,
        "next_page": "https://api.scryfall.com/cards?page=4",
        "data": [
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
              "highres_image": false,
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
              "reserved": false,
              "foil": true,
              "nonfoil": true,
              "oversized": false,
              "promo": false,
              "reprint": true,
              "set": "uma",
              "set_name": "Ultimate Masters",
              "set_uri": "https://api.scryfall.com/sets/2ec77b94-6d47-4891-a480-5d0b4e5c9372",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Auma&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/uma?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/9472cd09-0b0a-49c9-ab10-ec5b73ddb74b/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A2aa0e0e5-cb6d-4518-8eff-d29f935486e0&unique=prints",
              "collector_number": "175",
              "digital": false,
              "rarity": "rare",
              "illustration_id": "f1677113-e1ad-440c-9ca2-c15ba83e609a",
              "artist": "Greg Staples",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": false,
              "timeshifted": false,
              "colorshifted": false,
              "futureshifted": false,
              "story_spotlight": false,
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
              "highres_image": false,
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
              "reserved": false,
              "foil": true,
              "nonfoil": true,
              "oversized": false,
              "promo": false,
              "reprint": true,
              "set": "uma",
              "set_name": "Ultimate Masters",
              "set_uri": "https://api.scryfall.com/sets/2ec77b94-6d47-4891-a480-5d0b4e5c9372",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Auma&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/uma?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/ab0d006b-d783-4f63-a3e0-64df98a8b0db/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A2aa0e0e5-cb6d-4518-8eff-d29f935486e0&unique=prints",
              "collector_number": "175",
              "digital": false,
              "rarity": "rare",
              "illustration_id": "f1677113-e1ad-440c-9ca2-c15ba83e609a",
              "artist": "Greg Staples",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": false,
              "timeshifted": false,
              "colorshifted": false,
              "futureshifted": false,
              "story_spotlight": false,
              "edhrec_rank": 11876,
              "related_uris": {
                "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=457025&printed=true",
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
              "highres_image": true,
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
              "reserved": false,
              "foil": true,
              "nonfoil": true,
              "oversized": false,
              "promo": false,
              "reprint": true,
              "set": "uma",
              "set_name": "Ultimate Masters",
              "set_uri": "https://api.scryfall.com/sets/2ec77b94-6d47-4891-a480-5d0b4e5c9372",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Auma&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/uma?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/ff782973-e33c-4edd-bbd7-5c8dc8d59554/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A98aa9424-5912-4bd6-9300-b3972a31d8af&unique=prints",
              "collector_number": "174",
              "digital": false,
              "rarity": "rare",
              "flavor_text": "She protects the sacred groves from blight, drought, and the Unbeholden.",
              "illustration_id": "0a2b9149-9ff1-4097-8377-f3db60ef7ba8",
              "artist": "Mark Zug",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": false,
              "timeshifted": false,
              "colorshifted": false,
              "futureshifted": false,
              "story_spotlight": false,
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
              "highres_image": true,
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
              "reserved": false,
              "foil": true,
              "nonfoil": true,
              "oversized": false,
              "promo": false,
              "reprint": false,
              "set": "emn",
              "set_name": "Eldritch Moon",
              "set_uri": "https://api.scryfall.com/sets/5f0e4093-334f-4439-bbb5-a0affafd0ffc",
              "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aemn&unique=prints",
              "scryfall_set_uri": "https://scryfall.com/sets/emn?utm_source=api",
              "rulings_uri": "https://api.scryfall.com/cards/0900e494-962d-48c6-8e78-66a489be4bb2/rulings",
              "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A7cb29569-48e1-4782-9906-fad155ebfafe&unique=prints",
              "collector_number": "130a",
              "digital": false,
              "rarity": "rare",
              "flavor_text": "\"We're ready for anything!\"",
              "illustration_id": "2b2d858a-8c54-413a-a107-cfc587540ac9",
              "artist": "Vincent Proce",
              "border_color": "black",
              "frame": "2015",
              "frame_effect": "",
              "full_art": false,
              "story_spotlight": false,
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
    }'''.encode('utf_8'),
    'cards_search': r'''{
      "object": "list",
      "total_cards": 254,
      "has_more": true,
      "next_page": "https://api.scryfall.com/cards/search?format=json&include_extras=false&include_multilingual=false&order=name&page=2&q=set%3Aktk&unique=cards",
      "data": [
        {
          "object": "card",
          "id": "7df9759e-1072-4a6a-be57-f73b15bf3847",
          "oracle_id": "3d98af5f-7a0b-4a5a-b3e4-f3c9d150c993",
          "multiverse_ids": [
            386463
          ],
          "mtgo_id": 54416,
          "mtgo_foil_id": 54417,
          "tcgplayer_id": 93184,
          "name": "Abomination of Gudul",
          "lang": "en",
          "released_at": "2014-09-26",
          "uri": "https://api.scryfall.com/cards/7df9759e-1072-4a6a-be57-f73b15bf3847",
          "scryfall_uri": "https://scryfall.com/card/ktk/159/abomination-of-gudul?utm_source=api",
          "layout": "normal",
          "highres_image": true,
          "image_uris": {
            "small": "https://img.scryfall.com/cards/small/en/ktk/159.jpg?1517813031",
            "normal": "https://img.scryfall.com/cards/normal/en/ktk/159.jpg?1517813031",
            "large": "https://img.scryfall.com/cards/large/en/ktk/159.jpg?1517813031",
            "png": "https://img.scryfall.com/cards/png/en/ktk/159.png?1517813031",
            "art_crop": "https://img.scryfall.com/cards/art_crop/en/ktk/159.jpg?1517813031",
            "border_crop": "https://img.scryfall.com/cards/border_crop/en/ktk/159.jpg?1517813031"
          },
          "mana_cost": "{3}{B}{G}{U}",
          "cmc": 6.0,
          "type_line": "Creature — Horror",
          "oracle_text": "Flying\nWhenever Abomination of Gudul deals combat damage to a player, you may draw a card. If you do, discard a card.\nMorph {2}{B}{G}{U} (You may cast this card face down as a 2/2 creature for {3}. Turn it face up any time for its morph cost.)",
          "power": "3",
          "toughness": "4",
          "colors": [
            "B",
            "G",
            "U"
          ],
          "color_identity": [
            "B",
            "G",
            "U"
          ],
          "legalities": {
            "standard": "not_legal",
            "future": "not_legal",
            "frontier": "legal",
            "modern": "legal",
            "legacy": "legal",
            "pauper": "legal",
            "vintage": "legal",
            "penny": "legal",
            "commander": "legal",
            "1v1": "legal",
            "duel": "legal",
            "brawl": "not_legal"
          },
          "games": [
            "mtgo",
            "paper"
          ],
          "reserved": false,
          "foil": true,
          "nonfoil": true,
          "oversized": false,
          "promo": false,
          "reprint": false,
          "set": "ktk",
          "set_name": "Khans of Tarkir",
          "set_uri": "https://api.scryfall.com/sets/6c7a715c-ded9-449e-89b0-c665773e9c3c",
          "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aktk&unique=prints",
          "scryfall_set_uri": "https://scryfall.com/sets/ktk?utm_source=api",
          "rulings_uri": "https://api.scryfall.com/cards/7df9759e-1072-4a6a-be57-f73b15bf3847/rulings",
          "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A3d98af5f-7a0b-4a5a-b3e4-f3c9d150c993&unique=prints",
          "collector_number": "159",
          "digital": false,
          "rarity": "common",
          "watermark": "sultai",
          "illustration_id": "ef59d0ae-0b5d-422b-ad71-8fd66ddadd47",
          "artist": "Erica Yang",
          "border_color": "black",
          "frame": "2015",
          "frame_effect": "",
          "full_art": false,
          "story_spotlight": false,
          "edhrec_rank": 13859,
          "usd": "0.03",
          "eur": "0.02",
          "tix": "0.01",
          "related_uris": {
            "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=386463",
            "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Abomination+of+Gudul&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "edhrec": "http://edhrec.com/route/?cc=Abomination+of+Gudul",
            "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Abomination+of+Gudul"
          },
          "purchase_uris": {
            "tcgplayer": "https://shop.tcgplayer.com/magic/khans-of-tarkir/abomination-of-gudul?partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "cardmarket": "https://www.cardmarket.com/en/Magic/Products/Singles/Khans-of-Tarkir/Abomination-of-Gudul?referrer=scryfall",
            "cardhoarder": "https://www.cardhoarder.com/cards/54416?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
          }
        },
        {
          "object": "card",
          "id": "9af53a53-d30a-4289-a043-953cd81ee241",
          "oracle_id": "3b7d4206-0d88-407b-ace5-d5d28881bf95",
          "multiverse_ids": [
            386464
          ],
          "mtgo_id": 54426,
          "mtgo_foil_id": 54427,
          "tcgplayer_id": 92839,
          "name": "Abzan Ascendancy",
          "lang": "en",
          "released_at": "2014-09-26",
          "uri": "https://api.scryfall.com/cards/9af53a53-d30a-4289-a043-953cd81ee241",
          "scryfall_uri": "https://scryfall.com/card/ktk/160/abzan-ascendancy?utm_source=api",
          "layout": "normal",
          "highres_image": true,
          "image_uris": {
            "small": "https://img.scryfall.com/cards/small/en/ktk/160.jpg?1517813031",
            "normal": "https://img.scryfall.com/cards/normal/en/ktk/160.jpg?1517813031",
            "large": "https://img.scryfall.com/cards/large/en/ktk/160.jpg?1517813031",
            "png": "https://img.scryfall.com/cards/png/en/ktk/160.png?1517813031",
            "art_crop": "https://img.scryfall.com/cards/art_crop/en/ktk/160.jpg?1517813031",
            "border_crop": "https://img.scryfall.com/cards/border_crop/en/ktk/160.jpg?1517813031"
          },
          "mana_cost": "{W}{B}{G}",
          "cmc": 3.0,
          "type_line": "Enchantment",
          "oracle_text": "When Abzan Ascendancy enters the battlefield, put a +1/+1 counter on each creature you control.\nWhenever a nontoken creature you control dies, create a 1/1 white Spirit creature token with flying.",
          "colors": [
            "B",
            "G",
            "W"
          ],
          "color_identity": [
            "B",
            "G",
            "W"
          ],
          "all_parts": [
            {
              "object": "related_card",
              "id": "9af53a53-d30a-4289-a043-953cd81ee241",
              "component": "combo_piece",
              "name": "Abzan Ascendancy",
              "type_line": "Enchantment",
              "uri": "https://api.scryfall.com/cards/9af53a53-d30a-4289-a043-953cd81ee241"
            },
            {
              "object": "related_card",
              "id": "7071930c-689a-44b9-b52d-45027fd14446",
              "component": "token",
              "name": "Spirit",
              "type_line": "Token Creature — Spirit",
              "uri": "https://api.scryfall.com/cards/7071930c-689a-44b9-b52d-45027fd14446"
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
            "penny": "legal",
            "commander": "legal",
            "1v1": "legal",
            "duel": "legal",
            "brawl": "not_legal"
          },
          "games": [
            "mtgo",
            "paper"
          ],
          "reserved": false,
          "foil": true,
          "nonfoil": true,
          "oversized": false,
          "promo": false,
          "reprint": false,
          "set": "ktk",
          "set_name": "Khans of Tarkir",
          "set_uri": "https://api.scryfall.com/sets/6c7a715c-ded9-449e-89b0-c665773e9c3c",
          "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aktk&unique=prints",
          "scryfall_set_uri": "https://scryfall.com/sets/ktk?utm_source=api",
          "rulings_uri": "https://api.scryfall.com/cards/9af53a53-d30a-4289-a043-953cd81ee241/rulings",
          "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A3b7d4206-0d88-407b-ace5-d5d28881bf95&unique=prints",
          "collector_number": "160",
          "digital": false,
          "rarity": "rare",
          "watermark": "abzan",
          "illustration_id": "f0e9fd90-a137-4d57-b0c9-3cb3e51e1a18",
          "artist": "Mark Winters",
          "border_color": "black",
          "frame": "2015",
          "frame_effect": "",
          "full_art": false,
          "story_spotlight": false,
          "edhrec_rank": 3002,
          "usd": "0.24",
          "eur": "0.16",
          "tix": "0.01",
          "related_uris": {
            "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=386464",
            "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Abzan+Ascendancy&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "edhrec": "http://edhrec.com/route/?cc=Abzan+Ascendancy",
            "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Abzan+Ascendancy"
          },
          "purchase_uris": {
            "tcgplayer": "https://shop.tcgplayer.com/magic/khans-of-tarkir/abzan-ascendancy?partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "cardmarket": "https://www.cardmarket.com/en/Magic/Products/Singles/Khans-of-Tarkir/Abzan-Ascendancy?referrer=scryfall",
            "cardhoarder": "https://www.cardhoarder.com/cards/54426?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
          }
        },
        {
          "object": "card",
          "id": "7855528a-ede9-49a9-8749-795a004fd927",
          "oracle_id": "46535f8e-1bcd-4588-ac6c-a4bc89c379c8",
          "multiverse_ids": [
            386465
          ],
          "mtgo_id": 54060,
          "mtgo_foil_id": 54061,
          "tcgplayer_id": 93017,
          "name": "Abzan Banner",
          "lang": "en",
          "released_at": "2014-09-26",
          "uri": "https://api.scryfall.com/cards/7855528a-ede9-49a9-8749-795a004fd927",
          "scryfall_uri": "https://scryfall.com/card/ktk/215/abzan-banner?utm_source=api",
          "layout": "normal",
          "highres_image": true,
          "image_uris": {
            "small": "https://img.scryfall.com/cards/small/en/ktk/215.jpg?1517813031",
            "normal": "https://img.scryfall.com/cards/normal/en/ktk/215.jpg?1517813031",
            "large": "https://img.scryfall.com/cards/large/en/ktk/215.jpg?1517813031",
            "png": "https://img.scryfall.com/cards/png/en/ktk/215.png?1517813031",
            "art_crop": "https://img.scryfall.com/cards/art_crop/en/ktk/215.jpg?1517813031",
            "border_crop": "https://img.scryfall.com/cards/border_crop/en/ktk/215.jpg?1517813031"
          },
          "mana_cost": "{3}",
          "cmc": 3.0,
          "type_line": "Artifact",
          "oracle_text": "{T}: Add {W}, {B}, or {G}.\n{W}{B}{G}, {T}, Sacrifice Abzan Banner: Draw a card.",
          "colors": [

          ],
          "color_identity": [
            "B",
            "G",
            "W"
          ],
          "legalities": {
            "standard": "not_legal",
            "future": "not_legal",
            "frontier": "legal",
            "modern": "legal",
            "legacy": "legal",
            "pauper": "legal",
            "vintage": "legal",
            "penny": "legal",
            "commander": "legal",
            "1v1": "legal",
            "duel": "legal",
            "brawl": "not_legal"
          },
          "games": [
            "mtgo",
            "paper"
          ],
          "reserved": false,
          "foil": true,
          "nonfoil": true,
          "oversized": false,
          "promo": false,
          "reprint": false,
          "set": "ktk",
          "set_name": "Khans of Tarkir",
          "set_uri": "https://api.scryfall.com/sets/6c7a715c-ded9-449e-89b0-c665773e9c3c",
          "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aktk&unique=prints",
          "scryfall_set_uri": "https://scryfall.com/sets/ktk?utm_source=api",
          "rulings_uri": "https://api.scryfall.com/cards/7855528a-ede9-49a9-8749-795a004fd927/rulings",
          "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A46535f8e-1bcd-4588-ac6c-a4bc89c379c8&unique=prints",
          "collector_number": "215",
          "digital": false,
          "rarity": "common",
          "watermark": "abzan",
          "flavor_text": "Stone to endure, roots to remember.",
          "illustration_id": "659ad214-1586-4f7d-b17c-545980c75b2b",
          "artist": "Daniel Ljunggren",
          "border_color": "black",
          "frame": "2015",
          "frame_effect": "",
          "full_art": false,
          "story_spotlight": false,
          "edhrec_rank": 4299,
          "usd": "0.07",
          "eur": "0.10",
          "tix": "0.01",
          "related_uris": {
            "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=386465",
            "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Abzan+Banner&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "edhrec": "http://edhrec.com/route/?cc=Abzan+Banner",
            "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Abzan+Banner"
          },
          "purchase_uris": {
            "tcgplayer": "https://shop.tcgplayer.com/magic/khans-of-tarkir/abzan-banner?partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "cardmarket": "https://www.cardmarket.com/en/Magic/Products/Singles/Khans-of-Tarkir/Abzan-Banner?referrer=scryfall",
            "cardhoarder": "https://www.cardhoarder.com/cards/54060?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
          }
        },
        {
          "object": "card",
          "id": "8f5427b1-f1c2-4bb3-8736-701667ac2256",
          "oracle_id": "1b44fe0a-4a99-4166-b0b3-102b36b54ffa",
          "multiverse_ids": [
            386466
          ],
          "mtgo_id": 54276,
          "mtgo_foil_id": 54277,
          "tcgplayer_id": 93038,
          "name": "Abzan Battle Priest",
          "lang": "en",
          "released_at": "2014-09-26",
          "uri": "https://api.scryfall.com/cards/8f5427b1-f1c2-4bb3-8736-701667ac2256",
          "scryfall_uri": "https://scryfall.com/card/ktk/1/abzan-battle-priest?utm_source=api",
          "layout": "normal",
          "highres_image": true,
          "image_uris": {
            "small": "https://img.scryfall.com/cards/small/en/ktk/1.jpg?1517813031",
            "normal": "https://img.scryfall.com/cards/normal/en/ktk/1.jpg?1517813031",
            "large": "https://img.scryfall.com/cards/large/en/ktk/1.jpg?1517813031",
            "png": "https://img.scryfall.com/cards/png/en/ktk/1.png?1517813031",
            "art_crop": "https://img.scryfall.com/cards/art_crop/en/ktk/1.jpg?1517813031",
            "border_crop": "https://img.scryfall.com/cards/border_crop/en/ktk/1.jpg?1517813031"
          },
          "mana_cost": "{3}{W}",
          "cmc": 4.0,
          "type_line": "Creature — Human Cleric",
          "oracle_text": "Outlast {W} ({W}, {T}: Put a +1/+1 counter on this creature. Outlast only as a sorcery.)\nEach creature you control with a +1/+1 counter on it has lifelink.",
          "power": "3",
          "toughness": "2",
          "colors": [
            "W"
          ],
          "color_identity": [
            "W"
          ],
          "legalities": {
            "standard": "not_legal",
            "future": "not_legal",
            "frontier": "legal",
            "modern": "legal",
            "legacy": "legal",
            "pauper": "not_legal",
            "vintage": "legal",
            "penny": "legal",
            "commander": "legal",
            "1v1": "legal",
            "duel": "legal",
            "brawl": "not_legal"
          },
          "games": [
            "mtgo",
            "paper"
          ],
          "reserved": false,
          "foil": true,
          "nonfoil": true,
          "oversized": false,
          "promo": false,
          "reprint": false,
          "set": "ktk",
          "set_name": "Khans of Tarkir",
          "set_uri": "https://api.scryfall.com/sets/6c7a715c-ded9-449e-89b0-c665773e9c3c",
          "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Aktk&unique=prints",
          "scryfall_set_uri": "https://scryfall.com/sets/ktk?utm_source=api",
          "rulings_uri": "https://api.scryfall.com/cards/8f5427b1-f1c2-4bb3-8736-701667ac2256/rulings",
          "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A1b44fe0a-4a99-4166-b0b3-102b36b54ffa&unique=prints",
          "collector_number": "1",
          "digital": false,
          "rarity": "uncommon",
          "watermark": "abzan",
          "flavor_text": "\"Wherever I walk, the ancestors walk too.\"",
          "illustration_id": "81e1eac8-32f6-4be3-b5c2-95f1cb95eb59",
          "artist": "Chris Rahn",
          "border_color": "black",
          "frame": "2015",
          "frame_effect": "",
          "full_art": false,
          "story_spotlight": false,
          "edhrec_rank": 2612,
          "usd": "0.10",
          "eur": "0.09",
          "tix": "0.01",
          "related_uris": {
            "gatherer": "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=386466",
            "tcgplayer_decks": "https://decks.tcgplayer.com/magic/deck/search?contains=Abzan+Battle+Priest&page=1&partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "edhrec": "http://edhrec.com/route/?cc=Abzan+Battle+Priest",
            "mtgtop8": "http://mtgtop8.com/search?MD_check=1&SB_check=1&cards=Abzan+Battle+Priest"
          },
          "purchase_uris": {
            "tcgplayer": "https://shop.tcgplayer.com/magic/khans-of-tarkir/abzan-battle-priest?partner=Scryfall&utm_campaign=affiliate&utm_medium=scryfall&utm_source=scryfall",
            "cardmarket": "https://www.cardmarket.com/en/Magic/Products/Singles/Khans-of-Tarkir/Abzan-Battle-Priest?referrer=scryfall",
            "cardhoarder": "https://www.cardhoarder.com/cards/54276?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
          }
        }
      ]
    }'''.encode('utf_8'),
}


def shutdown_server():
    """Shutdown the server."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/sets', methods=['GET',])
def sets():
    """Return a dummy set list."""
    head = {'Content-Type': 'application/json; charset=utf-8',}
    return (resp['sets'], head)


@app.route('/sets/mmq', methods=['GET',])
def sets_code():
    """Return dummy set details."""
    head = {'Content-Type': 'application/json; charset=utf-8',}
    return (resp['sets_code'], head)


@app.route('/cards', methods=['GET',])
def cards():
    """Return a dummy cards list."""
    head = {'Content-Type': 'application/json; charset=utf-8',}
    return (resp['cards'], head)


@app.route('/cards/search', methods=['GET',])
def cards_search():
    """Return a dummy cards list."""
    head = {'Content-Type': 'application/json; charset=utf-8',}
    return (resp['cards_search'], head)


@app.route('/shutdown', methods=['GET',])
def shutdown():
    """Process request to shutdown the server."""
    shutdown_server()
    return 'Shutting down'


if __name__ == '__main__':
    app.run(debug=True)
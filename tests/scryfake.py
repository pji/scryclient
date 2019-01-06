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


@app.route('/cards', methods=['GET',])
def cards():
    """Return a dummy cards list."""
    head = {'Content-Type': 'application/json; charset=utf-8',}
    return (resp['cards'], head)


@app.route('/shutdown', methods=['GET',])
def shutdown():
    """Process request to shutdown the server."""
    shutdown_server()
    return 'Shutting down'


if __name__ == '__main__':
    app.run(debug=True)
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
resp = {'sets': b'''{
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
}''',}


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


@app.route('/shutdown', methods=['GET'])
def shutdown():
    """Process request to shutdown the server."""
    shutdown_server()
    return 'Shutting down'


if __name__ == '__main__':
    app.run(debug=True)
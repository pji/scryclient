scrycli Requirements Documentation
==================================

The purpose of this document is to detail the requirements for the 
scrycli module. This is an initial take to help with planning. There 
may be additional requirements or non-required features added in 
the future.


Purpose
-------
The scrycli module has two purposes:

* To be a partially implemented client for the Scryfall.com API
* To explore building unit tests for an API client
* To explore implementing trust boundaries in Python


Functional Requirements
-----------------------
The following are the functional requirements for scrycli:

1. scrycli can fetch a list of Magic: the Gathering (MtG) card sets 
   from Scryfall.com.
2. scrycli can fetch a list of MtG cards in a set from Scryfall.com.
3. These sets and cards can be integrated into a larger system for 
   storing information on a card collection.


Technical Requirements
----------------------
The following are the technical requirements for scrycli:

1. scrycli is a Python module.
2. scrycli uses the Requests module for HTTP.
3. scrycli uses the unittest module for unit testing.
4. scrycli uses Flask to create a dummy version of Scryfall.com for 
   unit tests.


Design Discussion
-----------------
The problem I'm having with this design is that I'm gathering data 
without knowing what I'm gathering it for. The input side of the 
system is defined, but I don't know what the best format is for the 
output side. That makes it very easy to just build the scrycli to 
return the native Python types for the JSON it receives from the 
API and call it a day but difficult to know whether that's the right 
answer. Maybe it's worth talking through this a bit.

Why am I pulling data from Scryfall.com?
    I have a collection of MtG cards. I'd like to know what I have 
    without needing to pull out the physical card boxes. I'd like 
    to have a database that stores that information and allows me 
    to look up the following:
    
    * Which cards in a set I have.
    * Which cards in a set I don't have.
    * How many of each card I have.
    * Where each of those cards are.
    * The stats on the card.

What information am I getting for the database from Scryfall.com?
    I'm getting the Scryfall.com data in order to:
    
    * Avoid having to manually type card stats into the database.
    * To know which cards I don't have.
    * To know the stats of the cards I don't have.

How will the collection system use scrycli?
    Based on the information the collection system will need, it 
    seems like scrycli will have the following use cases:
    
    1. User needs to know what sets they can get information for 
       from Scryfall.com.
    2. User needs to get a list of cards in a set.
    3. User needs to get the stats of a card in a set.
    
    This likely breaks down to the following API:
    
    * scrycli.get_sets() -> list
    * scrycli.get_cards(set) -> list
    * scrycli.get_cardstats(set, card) -> dict
    
    It does not seem like we are doing anything other than pulling 
    the data for the collection system to store, so we don't need 
    to create any custom classes for the data. Standard Python 
    data types will work just fine.
    
How will we separate the scrycli API from the Scryfall.com API?
    There does need to be a separation between the calls above and 
    the calls to Scryfall.com. This helps if Scryfall's API ever 
    changes or we need to use a different MtG card info repository. 
    
    I could do this with two objects:
    
    * A Scryfall.com API client object
    * A card data service API object
    
    However, there doesn't seem to be any data that persists across 
    multiple calls to get card data. At least, there is none that 
    would persist on the scrycli side. The persisting data would 
    be on the card collection side. So, custom objects seems like 
    overkill.
    
    Maybe instead, we go with two modules:
    
    * A Scryfall.com API client module
    * A "connector" module to provide a generic card data API for the 
      collection system to use.
    
    It's possible I should be designing the collection system first, 
    and providing an abstract base class for the connector there. 
    I'll revisit that question if/when I go back and design the 
    collection system.

Should scrycli have some sort of built-in user client?
    I'm not going to work on the collection system yet, so should 
    there be some other way for a user to use scrycli directly that 
    is built into scrycli? Probably. I'll add a simple CLI client 
    to at least show it's possible to have a client for this. It 
    also will avoid confusion with the "cli" at the end of scrycli. 
    
    That brings us to three modules:
    
    * scrycli
    * connector
    * cli
    
How do I handle redirecting scrycli during testing?
    During unit testing, scrycli needs to know to point to scryfake 
    rather than Scryfall. Handling that with a keyword parameter on 
    each function in scrycli seems redundant. That probably means 
    scrycli needs a configuration system of some sort. I don't know 
    if there is a best way to implement that.
    
    After a bit of searching, it looks like I am doing this wrong. 
    I should probably be using mock to mock rather than standing up 
    a mockup of the service using flask. I'm going to keep going as 
    is for now, but I will probably come back to switch this to mock 
    in the future.
    
    Today, though, it looks like I can add a config module that will 
    store config values. I can import that into scrycli, and, when 
    testing, I'll handle changing the test URL inside the testing 
    module.
    
    And now I have four modules:
    
    * scrycli
    * connector
    * cli
    * config
    
Are there any trust boundaries?
    NOTE: With connector still unimplemented, the closest thing in 
    the current design is cli. The cli module does not implement 
    a trust boundary on input going into scrycli. That means these 
    tables are a little off from the current design, but the tables 
    are still the goal.
    
    Yes. I'm pulling data in from Scryfall.com. That data will need 
    to be validated before anything is done with it. Where should 
    that be done?
    
    First, though, what's the specific reason for the need for 
    validation here? I'm following reasoning pointed to in the 
    SEI CERT Java Secure Coding Guidelines: Myth of Trust. Yes, 
    it's Java not Python, but the patterns here should be generic. 
    The idea is that the patterns of distrustful decomposition and 
    privilege separation puts code with access to the network in 
    a different trust domain than code with access to other systems. 
    Code that crosses from one trust domain to another crosses a 
    trust boundary and must be validated.
    
    The call flow goes as follows:
    
        +-----------+----+--------------+-----------+
        | Client    | -> | connector    | Trusted   |
        +-----------+----+--------------+           |
        | connector | -> | scrycli      |           |
        +-----------+----+--------------+-----------+
        | scrycli   | -> | Scryfall.com | Untrusted |
        +-----------+----+--------------+           |
        | scrycli   | <- | Scryfall.com |           |
        +-----------+----+--------------+-----------+
        | connector | <- | scrycli      | Trusted   |
        +-----------+----+--------------+           |
        | Client    | <- | connector    |           |
        +-----------+----+--------------+-----------+
    
    It seems then that the trust boundary needs to sit between the 
    connector and the scrycli modules.
    
    The call flow is now:
    
        +-----------+----+--------------+-----------+
        | Client    | -> | connector    | Trusted   |
        +-----------+----+--------------+           |
        | connector | -> | validator    |           |
        +-----------+----+--------------+-----------+
        | validator | -> | scrycli      | Border    |
        +-----------+----+--------------+-----------+
        | scrycli   | -> | Scryfall.com | Untrusted |
        +-----------+----+--------------+           |
        | scrycli   | <- | Scryfall.com |           |
        +-----------+----+--------------+-----------+
        | validator | <- | scrycli      | Border    |
        +-----------+----+--------------+-----------+
        | connector | <- | validator    | Trusted*  |
        +-----------+----+--------------+           |
        | Client    | <- | connector    |           |
        +-----------+----+--------------+-----------+
        
        \* Within the limits of the validation.
    
    There are now five modules:
    
    * scrycli
    * connector
    * cli
    * config
    * validator

How should validator be implemented?
    It feels like this should be doable as a decorator. Perhaps it's 
    a trust_boundary() decorator that acts on the returning data? 
    I've never done it, but it should be possible.
    
    Three things need to happen during validation:
    
    *   Canonicalization
    *   Normalization
    *   Validation
    
    I want to limit understanding of the requests module to the 
    scrycli module. Can a decorator from a validator module do 
    these things without knowing the requests module?
    
    Canonicalization
        This is a lossless reduction of the input to its simplest 
        known form. Since I'm getting back a str from requests and 
        not a byte, we should already be in UTF-8. It's likely just 
        a matter of ensuring there is no encoding surprises, and 
        won't need requests.
    
    Normalization
        This is the lossy reduction of the input to its simplest 
        and anticipated form. This is the conversion from JSON to 
        Python types. This needs json, but it doesn't need requests.
    
    Validation
        This is checking to ensure the data is in expected ranges. 
        The requests module isn't needed here.
    
    So, it seems like the decorator can handle this. I just want to 
    make sure to heavily comment the return statements in scrycli's 
    functions to reduce the surprise factor when the decorator 
    changes the return type.
    
    The trust_boundary() function itself will likely need internal 
    functions for each of the functions in scrycli. Those may be 
    better implemented in scrycli itself, though. That would allow 
    validator to remain generic enough that it would be able to 
    be used for different MtG card data repositories if needed. Is 
    there a dispatch-type pattern that is useable for this?
    
    I'll probably hold off on solving how to register validation 
    functions for now and just link validator to scrycli.

How should this be reviewed?
    In order to assure these trust boundaries are not violated, 
    the following should be reviewed before each commit:
    
    *   No module other than scrycli imports requests or another 
        HTTP client module.
    *   Modules only call the public functions in scrycli.
    *   All public functions in scrycli are decorated with the 
        trust boundary decorator (currently: PV.trust_boundary).
    
    This is currently manual because my commits are manual. I'll 
    work on getting this automated in the future.
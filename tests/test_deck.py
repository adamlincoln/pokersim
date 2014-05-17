import copy
import simplejson as json

from pokersim.Deck import Deck

def test_deck_one():
    deck = Deck()
    assert len(deck.cards) == 52 

def test_deck_shuffle():
    deck = Deck()
    cards = copy.deepcopy(deck.cards)
    assert cards == deck.cards
    deck.shuffle()
    assert cards != deck.cards

def test_deck_deal_one():
    deck = Deck()
    remember = deck.cards[0]
    assert remember == deck.deal()
    assert len(deck.cards) == 51

def test_deck_deal_ten():
    deck = Deck()
    remember = deck.cards[:10]
    assert remember == deck.deal(10)
    assert len(deck.cards) == 42

def test_deck_deal_53():
    deck = Deck()
    for i in xrange(52):
        remember = deck.deal()
    try:
        remember = deck.deal()
    except IndexError as e:
        assert e.message == 'No cards left in deck'
    else:
        assert False

def test_deck_str():
    deck = Deck()
    deck.shuffle()
    before = str(deck)
    remember = []
    for i in xrange(52):
        remember.append(str(deck.deal()))
    assert before == json.dumps(remember)

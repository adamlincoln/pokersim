import copy

from pokersim.Deck import Deck

def test_deck_one():
    deck = Deck()
    assert len(deck.cards) == 52 

def test_deck_two():
    deck = Deck()
    cards = copy.deepcopy(deck.cards)
    assert cards == deck.cards
    deck.shuffle()
    assert cards != deck.cards

def test_deck_three():
    deck = Deck()
    remember = deck.cards[0]
    assert remember == deck.deal()
    assert len(deck.cards) == 51

def test_deck_four():
    deck = Deck()
    remember = deck.cards[:10]
    assert remember == deck.deal(10)
    assert len(deck.cards) == 42

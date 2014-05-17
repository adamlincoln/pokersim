from pokersim.Card import Card

def test_blank_card():
    card = Card()
    assert card.suit is None
    assert card.value is None

def test_single_card():
    card = Card('H', '10')
    assert card.suit == 'H'
    assert card.value == '10'

def test_card_equality():
    card1 = Card('C', 'J')
    card2 = Card('C', 'J')
    assert card1 == card2

def test_card_inequality():
    card1 = Card('C', 'J')
    card2 = Card('C', 'Q')
    assert card1 != card2

def test_card_string():
    card1 = Card('C', 'J')
    assert str(card1) == 'JC'

def test_card_repr():
    card1 = Card('C', '10')
    assert repr(card1) == '<Card 10C>'


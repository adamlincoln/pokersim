from pokersim.Card import Card

def test_blank_card():
    card = Card()
    assert card.suit is None
    assert card.value is None

def test_single_card():
    card = Card('H', '10')
    assert card.suit == 'H'
    assert card.value == 10

def test_single_card_int_value():
    card = Card('H', 10)
    assert card.suit == 'H'
    assert card.value == 10

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

def test_card_cmp_value():
    card1 = Card('C', '10')
    card2 = Card('C', 'Q')
    assert card1.cmp_value(card2) < 0
    assert card2.cmp_value(card1) > 0

def test_card_sort_with_cmp_value():
    cards = [Card('C', '10'), Card('S', '2'), Card('C', '5'), Card('S', 'A'), Card('H', 'K'), Card('D', 'K'), ]
    cards.sort(cmp = Card.cmp_value)
    assert cards == [Card('S', '2'), Card('C', '5'), Card('C', '10'), Card('H', 'K'), Card('D', 'K'), Card('S', 'A')]

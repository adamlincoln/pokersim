from pokersim.Card import Card

def test_card_one():
    card = Card()
    assert card.suit is None
    assert card.value is None

def test_card_two():
    card = Card('H', '10')
    assert card.suit == 'H'
    assert card.value == '10'

def test_card_three():
    card1 = Card('C', 'J')
    card2 = Card('C', 'J')
    assert card1 == card2


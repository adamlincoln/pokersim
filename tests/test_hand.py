from pokersim.Hand import Hand
from pokersim.Card import Card

def test_hand_high_card_one():
    hand1 = Hand([
        Card('H', '2'),
        Card('H', '5'),
        Card('C', '6'),
        Card('H', 'Q'),
        Card('D', 'A')
    ])
    hand2 = Hand([
        Card('H', '3'),
        Card('H', '7'),
        Card('C', '8'),
        Card('C', '2'),
        Card('D', 'K')
    ])
    assert hand1 > hand2

def test_hand_pair_vs_high_card():
    hand1 = Hand([
        Card('H', '2'),
        Card('H', '5'),
        Card('C', 'K'),
        Card('H', 'Q'),
        Card('D', 'A')
    ])
    hand2 = Hand([
        Card('H', '3'),
        Card('C', '3'),
        Card('C', '8'),
        Card('C', '2'),
        Card('D', 'K')
    ])
    assert hand1 < hand2

def test_hand_pair_one():
    hand1 = Hand([
        Card('H', '2'),
        Card('H', '5'),
        Card('C', 'Q'),
        Card('H', 'Q'),
        Card('D', 'A')
    ])
    hand2 = Hand([
        Card('H', '3'),
        Card('C', '3'),
        Card('C', '8'),
        Card('C', '2'),
        Card('D', 'K')
    ])
    assert hand1 > hand2

def test_hand_pair_two():
    hand1 = Hand([
        Card('H', '3'),
        Card('C', '3'),
        Card('H', '2'),
        Card('H', '5'),
        Card('D', 'A')
    ])
    hand2 = Hand([
        Card('C', 'Q'),
        Card('H', 'Q'),
        Card('C', '8'),
        Card('C', '2'),
        Card('D', 'K')
    ])
    assert hand1 < hand2

def test_hand_pair_kicker():
    hand1 = Hand([
        Card('H', '2'),
        Card('H', '5'),
        Card('C', 'Q'),
        Card('H', 'Q'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('H', '10'),
        Card('C', '4'),
        Card('S', 'Q'),
        Card('C', '2'),
        Card('D', 'Q')
    ])
    assert hand1 < hand2

def test_hand_two_pair_beats_one_pair():
    hand1 = Hand([
        Card('D', '5'),
        Card('H', '5'),
        Card('C', 'Q'),
        Card('H', 'Q'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('H', '10'),
        Card('C', '4'),
        Card('S', 'A'),
        Card('C', '2'),
        Card('D', 'A')
    ])
    assert hand1 > hand2

def test_hand_two_pair_top_wins():
    hand1 = Hand([
        Card('D', '5'),
        Card('H', '5'),
        Card('C', 'Q'),
        Card('H', 'Q'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('H', '4'),
        Card('C', '4'),
        Card('S', 'A'),
        Card('C', '2'),
        Card('D', 'A')
    ])
    assert hand1 < hand2

def test_hand_two_pair_bottom_wins():
    hand1 = Hand([
        Card('D', '5'),
        Card('H', '5'),
        Card('C', 'Q'),
        Card('H', 'Q'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('H', '4'),
        Card('C', '4'),
        Card('S', 'Q'),
        Card('C', '2'),
        Card('D', 'Q')
    ])
    assert hand1 > hand2

def test_hand_two_pair_kicker_wins():
    hand1 = Hand([
        Card('D', '5'),
        Card('H', '5'),
        Card('C', 'Q'),
        Card('H', 'Q'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('S', '5'),
        Card('C', '5'),
        Card('S', 'Q'),
        Card('C', '2'),
        Card('D', 'Q')
    ])
    assert hand1 > hand2

def test_hand_three_of_a_kind_beats_two_pair():
    hand1 = Hand([
        Card('D', '5'),
        Card('H', '5'),
        Card('C', '5'),
        Card('H', 'Q'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('H', '4'),
        Card('C', '4'),
        Card('S', 'A'),
        Card('C', '2'),
        Card('D', 'A')
    ])
    assert hand1 > hand2

def test_hand_three_of_a_kind_value_wins():
    hand1 = Hand([
        Card('D', '5'),
        Card('H', '5'),
        Card('C', '5'),
        Card('H', 'Q'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('H', '4'),
        Card('C', '7'),
        Card('S', 'A'),
        Card('C', 'A'),
        Card('D', 'A')
    ])
    assert hand1 < hand2

def test_hand_straight_beats_three_of_a_kind():
    hand1 = Hand([
        Card('D', '7'),
        Card('H', '6'),
        Card('C', '5'),
        Card('H', '4'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('S', '4'),
        Card('C', '7'),
        Card('S', 'A'),
        Card('C', 'A'),
        Card('D', 'A')
    ])
    assert hand1 > hand2

def test_hand_ace_low_straight_beats_three_of_a_kind():
    hand1 = Hand([
        Card('D', '5'),
        Card('H', '4'),
        Card('C', '3'),
        Card('H', '2'),
        Card('D', 'A')
    ])
    hand2 = Hand([
        Card('S', '4'),
        Card('C', '7'),
        Card('S', 'A'),
        Card('C', 'A'),
        Card('D', 'A')
    ])
    assert hand1 > hand2

def test_hand_straight_high_card_wins():
    hand1 = Hand([
        Card('D', '7'),
        Card('H', '6'),
        Card('C', '5'),
        Card('H', '4'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('S', '7'),
        Card('C', '8'),
        Card('S', '9'),
        Card('C', '10'),
        Card('D', 'J')
    ])
    assert hand1 < hand2

def test_hand_straight_ace_high_wins():
    hand1 = Hand([
        Card('D', 'A'),
        Card('H', 'K'),
        Card('C', 'Q'),
        Card('H', 'J'),
        Card('D', '10')
    ])
    hand2 = Hand([
        Card('S', '7'),
        Card('C', '8'),
        Card('S', '9'),
        Card('C', '10'),
        Card('D', 'J')
    ])
    assert hand1 > hand2

def test_hand_flush_beats_straight():
    hand1 = Hand([
        Card('D', 'A'),
        Card('H', 'K'),
        Card('C', 'Q'),
        Card('H', 'J'),
        Card('D', '10')
    ])
    hand2 = Hand([
        Card('S', 'J'),
        Card('S', '8'),
        Card('S', '6'),
        Card('S', '4'),
        Card('S', '2')
    ])
    assert hand1 < hand2

def test_hand_flush_kicker_one():
    hand1 = Hand([
        Card('D', '10'),
        Card('D', '7'),
        Card('D', '5'),
        Card('D', '4'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('S', 'J'),
        Card('S', '8'),
        Card('S', '6'),
        Card('S', '4'),
        Card('S', '2')
    ])
    assert hand1 < hand2

def test_hand_flush_kicker_two():
    hand1 = Hand([
        Card('D', 'J'),
        Card('D', '7'),
        Card('D', '5'),
        Card('D', '4'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('S', 'J'),
        Card('S', '8'),
        Card('S', '6'),
        Card('S', '4'),
        Card('S', '2')
    ])
    assert hand1 < hand2

def test_hand_flush_kicker_three():
    hand1 = Hand([
        Card('D', 'J'),
        Card('D', '8'),
        Card('D', '5'),
        Card('D', '4'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('S', 'J'),
        Card('S', '8'),
        Card('S', '6'),
        Card('S', '4'),
        Card('S', '2')
    ])
    assert hand1 < hand2

def test_hand_flush_kicker_four():
    hand1 = Hand([
        Card('D', 'J'),
        Card('D', '8'),
        Card('D', '5'),
        Card('D', '3'),
        Card('D', '2')
    ])
    hand2 = Hand([
        Card('S', 'J'),
        Card('S', '8'),
        Card('S', '5'),
        Card('S', '4'),
        Card('S', '2')
    ])
    assert hand1 < hand2

def test_hand_flush_kicker_five():
    hand1 = Hand([
        Card('D', 'J'),
        Card('D', '8'),
        Card('D', '6'),
        Card('D', '4'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('S', 'J'),
        Card('S', '8'),
        Card('S', '6'),
        Card('S', '4'),
        Card('S', '2')
    ])
    assert hand1 > hand2

def test_hand_full_house_beats_flush():
    hand1 = Hand([
        Card('D', 'J'),
        Card('D', '8'),
        Card('D', '6'),
        Card('D', '4'),
        Card('D', '3')
    ])
    hand2 = Hand([
        Card('S', '10'),
        Card('D', '10'),
        Card('H', '10'),
        Card('D', '2'),
        Card('S', '2')
    ])
    assert hand1 < hand2

def test_hand_full_house_high_triplet_wins():
    hand1 = Hand([
        Card('D', 'K'),
        Card('C', 'K'),
        Card('H', 'K'),
        Card('D', '2'),
        Card('S', '2')
    ])
    hand2 = Hand([
        Card('S', '10'),
        Card('D', '10'),
        Card('H', '10'),
        Card('D', '9'),
        Card('S', '9')
    ])
    assert hand1 > hand2

def test_hand_four_of_a_kind_beats_full_house():
    hand1 = Hand([
        Card('D', '4'),
        Card('H', '4'),
        Card('S', '4'),
        Card('C', '4'),
        Card('D', '9')
    ])
    hand2 = Hand([
        Card('S', '10'),
        Card('D', '10'),
        Card('H', '10'),
        Card('D', '2'),
        Card('S', '2')
    ])
    assert hand1 > hand2

def test_hand_four_of_a_kind_high_quad_wins():
    hand1 = Hand([
        Card('D', '4'),
        Card('H', '4'),
        Card('S', '4'),
        Card('C', '4'),
        Card('D', '9')
    ])
    hand2 = Hand([
        Card('S', '10'),
        Card('D', '10'),
        Card('H', '10'),
        Card('C', '10'),
        Card('S', '2')
    ])
    assert hand1 < hand2

def test_hand_straight_flush_beats_four_of_a_kind():
    hand1 = Hand([
        Card('D', '9'),
        Card('H', '9'),
        Card('S', '9'),
        Card('C', '9'),
        Card('D', 'K')
    ])
    hand2 = Hand([
        Card('S', '6'),
        Card('S', '5'),
        Card('S', '4'),
        Card('S', '3'),
        Card('S', '2')
    ])
    assert hand1 < hand2

def test_hand_straight_flush_highest_wins():
    hand1 = Hand([
        Card('H', '9'),
        Card('H', '8'),
        Card('H', '7'),
        Card('H', '6'),
        Card('H', '5')
    ])
    hand2 = Hand([
        Card('S', '6'),
        Card('S', '5'),
        Card('S', '4'),
        Card('S', '3'),
        Card('S', '2')
    ])
    assert hand1 > hand2

def test_hand_straight_tie():
    hand1 = Hand([
        Card('H', '9'),
        Card('H', '8'),
        Card('D', '7'),
        Card('H', '6'),
        Card('H', '5')
    ])
    hand2 = Hand([
        Card('H', '9'),
        Card('H', '8'),
        Card('S', '7'),
        Card('H', '6'),
        Card('H', '5')
    ])
    assert not hand1 > hand2
    assert not hand1 < hand2
    assert hand1 == hand2


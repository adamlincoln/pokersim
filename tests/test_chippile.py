from pokersim.ChipPile import ChipPile

def test_chippile():
    cp1 = ChipPile('ONE', 10)
    cp2 = ChipPile('TWO', 20)
    assert cp1.chips == 10
    assert cp2.chips == 20
    assert cp1.name == 'ONE'
    assert cp2.name == 'TWO'
    assert str(cp1) == 'ONE: 10'
    assert repr(cp2) == '<ChipPile TWO: 20 >'
    assert cp1 == ChipPile('something else', 10)

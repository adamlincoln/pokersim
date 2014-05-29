from pokersim.ChipConduit import ChipConduit
from pokersim.ChipPile import ChipPile

def test_chipconduit_ints():
    cp1 = ChipPile('test1', 10)
    cp2 = ChipPile('test2', 20)
    ChipConduit.move(8, cp1, 'chips', cp2, 'chips')
    assert cp1.name == 'test1'
    assert cp2.name == 'test2'
    assert cp1.chips == 2
    assert cp2.chips == 28

def some_func(amt, *other_args):
    frm = other_args[0]
    frm.chips = amt + 100
    frm.others = other_args[1]

def some_other_func(amt, *other_args):
    to = other_args[0]
    to.chips = amt + 2000
    to.others = other_args[1]

def test_chipconduit_callables():
    cp1 = ChipPile('test1', 10)
    cp2 = ChipPile('test2', 20)
    cp1.some_func = some_func
    cp2.some_func2 = some_other_func # Yeah, tricky eh?
    # Those functions are unbound to an object so they have to be passed in for the purposes of this test.
    ChipConduit.move(8, cp1, 'some_func', cp2, 'some_func2', frm_call_args=[cp1, 'ASTRING'], to_call_args=[cp2, 47])
    assert cp1.name == 'test1'
    assert cp2.name == 'test2'
    assert cp1.chips == 108
    assert cp1.others == 'ASTRING'
    assert cp2.chips == 2008
    assert cp2.others == 47

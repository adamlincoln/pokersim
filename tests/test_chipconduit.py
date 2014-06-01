from pokersim.ChipConduit import ChipConduit

class TestClass(object):
    pass

def test_chipconduit_dicts():
    cp1 = {1: 25, 2: 50}
    cp2 = {0: 125, 4: 5}
    ChipConduit.move(8, cp1, 2, cp2, 0)
    assert cp1 == {1: 25, 2: 42}
    assert cp2 == {0: 133, 4: 5} 

def test_chipconduit_dicts_zero_check():
    cp1 = {1: 25, 2: 50}
    cp2 = {0: 125, 4: 5}
    ChipConduit.move(108, cp1, 2, cp2, 0)
    assert cp1 == {1: 25, 2: 0}
    assert cp2 == {0: 175, 4: 5} 

def test_chipconduit_objects():
    cp1 = TestClass()
    cp1.chipssss = 109
    cp2 = TestClass()
    cp2.chips = 8
    ChipConduit.move(7, cp2, 'chips', cp1, 'chipssss')
    assert cp1.chipssss == 116
    assert cp2.chips == 1

def between(arg1, arg2):
    return arg1 + arg2, None

def test_chipconduit_between():
    cp1 = {1: 25, 2: 50}
    cp2 = TestClass()
    cp2.chips = 8
    returned = ChipConduit.move(8, cp1, 1, cp2, 'chips', between=between, between_args=(100, 209))
    assert cp1 == {1: 17, 2: 50}
    assert cp2.chips == 16
    assert returned == 309

def between2(arg1, arg2):
    return arg1 + arg2, {'amt': 2}

def test_chipconduit_between2():
    cp1 = {1: 25, 2: 50}
    cp2 = TestClass()
    cp2.chips = 8
    returned = ChipConduit.move(8, cp1, 1, cp2, 'chips', between=between2, between_args=(102, 209))
    assert cp1 == {1: 17, 2: 50}
    assert cp2.chips == 10
    assert returned == 311

#def test_chipconduit_ints():
    #cp1 = 10
    #cp2 = 20
    #ChipConduit.move(8, cp1, 'chips', cp2, 'chips')
    #assert cp1.name == 'test1'
    #assert cp2.name == 'test2'
    #assert cp1.chips == 2
    #assert cp2.chips == 28

def some_func(amt, *other_args):
    frm = other_args[0]
    frm.chips = amt + 100
    frm.others = other_args[1]

def some_other_func(amt, *other_args):
    to = other_args[0]
    to.chips = amt + 2000
    to.others = other_args[1]

def a_between_func(*other_args):
    setattr(other_args[0], other_args[1], 'some_value')

#def test_chipconduit_callables():
    #cp1 = 10
    #cp2 = 20
    #cp1.some_func = some_func
    #cp2.some_func2 = some_other_func # Yeah, tricky eh?
    ## Those functions are unbound to an object so they have to be passed in for the purposes of this test.
    #ChipConduit.move(
        #8,
        #cp1,
        #'some_func',
        #cp2,
        #'some_func2',
        #frm_call_args=[cp1, 'ASTRING'],
        #to_call_args=[cp2, 47],
        #between=a_between_func,
        #between_args=[cp1, 'some_attribute']
    #)
    #assert cp1.name == 'test1'
    #assert cp2.name == 'test2'
    #assert cp1.chips == 108
    #assert cp1.others == 'ASTRING'
    #assert cp2.chips == 2008
    #assert cp2.others == 47
    #assert cp1.some_attribute == 'some_value'

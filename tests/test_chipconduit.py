from pubsub import pub
from nose import with_setup

from pokersim.ChipConduit import ChipConduit

# Test level setup
heard = []
def listener(topicObj=pub.AUTO_TOPIC, **mesgData):
    heard.append((topicObj.getName(), mesgData))

def setup_each_test():
    pub.subscribe(listener, pub.ALL_TOPICS)

def teardown_each_test():
    del heard[:]
# End test level setup

class TestClass(object):
    pass

@with_setup(setup_each_test, teardown_each_test)
def test_chipconduit_dicts():
    cp1 = {1: 25, 2: 50}
    cp2 = {0: 125, 4: 5}
    ChipConduit.move(8, cp1, 2, cp2, 0)
    assert cp1 == {1: 25, 2: 42}
    assert cp2 == {0: 133, 4: 5} 
    assert heard == [('chip_movement', {'data': {'amt': 8}})]

@with_setup(setup_each_test, teardown_each_test)
def test_chipconduit_dicts_zero_check():
    cp1 = {1: 25, 2: 50}
    cp2 = {0: 125, 4: 5}
    ChipConduit.move(108, cp1, 2, cp2, 0, frm_tracking='cp1', to_tracking='cp2')
    assert cp1 == {1: 25, 2: 0}
    assert cp2 == {0: 175, 4: 5} 
    assert heard == [('chip_movement', {'data': {'amt': 50, 'from': 'cp1', 'to': 'cp2'}})]

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


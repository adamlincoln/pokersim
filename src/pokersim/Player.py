from pubsub import pub
from importlib import import_module

from Decision import Decision
from Bank import Bank

class Player(object):
    def __init__(self, chips, brain_implementation=None):
        self.leave()
        self.discard_hole_cards()
        self.brain = None
        if brain_implementation is not None:
            try:
                brain_module = import_module('.{0}'.format(brain_implementation), 'pokersim.brains')
            except ImportError:
                raise PlayerException('Brain named "{0}" cannot be found'.format(brain_implementation))
            else:
                self.brain = eval('brain_module.{0}'.format(brain_implementation))(self)
        if self.brain is not None and hasattr(self.brain, 'watcher'):
            pub.subscribe(self.brain.watcher, pub.ALL_TOPICS)
        if isinstance(chips, int):
            self.chips = Bank.makeNewChips(chips)
        else:
            self.chips = chips

    def sit(self, table, position):
        self.table = table
        self.position = position
        table.players[position] = self

    def leave(self):
        if hasattr(self, 'table') and self.table is not None:
            pub.sendMessage('leave', data={'table': self.table, 'position': self.position, 'chips': self.chips})
        self.table = None
        self.position = None

    def discard_hole_cards(self):
        self.hole_cards = []

    def __repr__(self):
        return '<Player Pos: {0}  Hole Cards: {1}  Chips: {2}>'.format(
            str(self.position) if self.position != None else '',
            ', '.join([repr(card) for card in self.hole_cards]),
            str(self.chips)
        )

    def decide(self, error=None, force=None):
        # Available to the player here is the current state of the table, plus any stuff he got via pubsub.
        if force is not None:
            return force
        if self.brain is not None and hasattr(self.brain, 'decider'):
            return self.brain.decider(self.table)
        else:
            return Decision.FOLD

class PlayerException(Exception):
    pass

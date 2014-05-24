from pubsub import pub
from itertools import combinations

from ..Brain import Brain
from ..Decision import Decision
from ..Hand import Hand

class FoldWithNoPostFlopPairOrBetter(Brain):
    def __init__(self, player):
        super(FoldWithNoPostFlopPairOrBetter, self).__init__(player)

    def watcher(self, topic=pub.AUTO_TOPIC, **data):
        pass

    def decider(self, table):
        if len(table.board) == 0:
            # Always see a flop
            return Decision.CALL
        else:
            for potential_hands in combinations(table.board + self.player.hole_cards, 5):
                hand = Hand(list(potential_hands))
                if hand.rank()['rank'] > 0:
                    return Decision.CALL
            return Decision.FOLD

from pubsub import pub
from itertools import combinations

from ..Brain import Brain
from ..Decision import Decision
from ..Hand import Hand

class CallPairOrBetter(Brain):
    def __init__(self, player):
        super(CallPairOrBetter, self).__init__(player)

    def watcher(self, topic=pub.AUTO_TOPIC, **data):
        pass

    def decider(self, table):
        if len(table.board) == 0:
            if self.player.hole_cards[0].value == self.player.hole_cards[1].value:
                return Decision.CALL
            else:
                return Decision.FOLD
        else:
            # If we get here, we already have a pocket pair
            return Decision.CALL

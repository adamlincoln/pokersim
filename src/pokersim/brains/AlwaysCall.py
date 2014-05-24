from pubsub import pub

from ..Brain import Brain
from ..Decision import Decision

class AlwaysCall(Brain):
    def watcher(self, topic=pub.AUTO_TOPIC, **data):
        pass

    def decider(self, table):
        return Decision.CALL

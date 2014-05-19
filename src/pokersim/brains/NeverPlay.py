from pubsub import pub

from ..Brain import Brain
from ..Decision import Decision

class NeverPlay(Brain):
    def watcher(self, topic=pub.AUTO_TOPIC, **data):
        super(NeverPlay, self).watcher(topic, **data)
        pass

    def decider(self, table):
        super(NeverPlay, self).decider(table)
        return Decision.FOLD

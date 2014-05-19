from abc import ABCMeta
from abc import abstractmethod
from pubsub import pub

class Brain(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def watcher(self, topic=pub.AUTO_TOPIC, **data):
        pass

    @abstractmethod
    def decider(self, table):
        pass

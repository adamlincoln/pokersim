from pubsub import pub
import sqlite3

class Recorder(object):
    def print_all_topics(self, topicObj=pub.AUTO_TOPIC, **mesgData):
        if 'to' in mesgData['data']:
            print 'topic "{0}": {1}'.format(topicObj.getName(), mesgData)

    def write_to_db(self, topicObj=pub.AUTO_TOPIC, **mesgData):
        if 'to' in mesgData['data']:
            c = self.db.cursor()
            

    def __init__(self):
        pub.subscribe(self.print_all_topics, pub.ALL_TOPICS)
        pub.subscribe(self.write_to_db, pub.ALL_TOPICS)
        self.db = sqlite3.connect(':memory:')

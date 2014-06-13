from Chip import Chip

class Bank(object):
    @staticmethod
    def makeNewChips(amt):
        return [Chip() for i in xrange(amt)]        

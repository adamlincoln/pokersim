import argparse

from pokersim.Table import Table
from pokersim.Player import Player

from pokersim.Recorder import Recorder

rec = Recorder()

parser = argparse.ArgumentParser(description='Set up a poker game')
#parser.add_argument('-n', '--numplayers', type=int, nargs='?', default=10, help='Number of players')
parser.add_argument('-d', '--numhands', type=int, nargs='?', default=1, help='Number of hands')
#parser.add_argument('-c', '--chips', action='append', type=int, nargs='+', help='Number of chips')
parser.add_argument('-p', '--players', action='append', nargs=2, metavar=('number_of_chips', 'brain_name'), help='Player info: chips brain_name')

def main():
    args = vars(parser.parse_args())
    print args
    # Get from command line:
    # Type of players
    # Chips for players

    numplayers = len(args['players'])
    if numplayers < 3:
        print 'At least 3 players are needed.  You selected', numplayers
        return

    #if args['chips'] is not None and len(args['chips']) > numplayers:
        #numplayers = len(args['chips'])
    table = Table()
    for i in xrange(numplayers):
        player = Player(int(args['players'][i][0]), args['players'][i][1])
        player.sit(table, i)
    for i in xrange(args['numhands']):
        table.deal()
    print 'After', args['numhands'], 'hands:'
    for player in table.players.values():
        print 'Player', player.position, 'has', player.chips, 'chips'
    print 'The Table has', table.box, 'chips'

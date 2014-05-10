import pokersim.Table

def main():
    table = pokersim.Table.Table()
    table.deal()

    import sys
    sys.exit()

    import pokersim.Deck

    deck = pokersim.Deck.Deck()
    print deck

    print deck.deal()

    print deck

    deck.shuffle()
    print deck

    print deck.deal()
    print deck
    print [str(card) for card in deck.deal(n=5)]
    print deck
    print deck.deal()
    print deck

LIMIT = 16


def dealer_play(hand, deck):
    """Dealer draws cards until they reach their limit."""
    while hand.value() < LIMIT:
        hand.add(deck.deal())
    return hand

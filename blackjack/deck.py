import random

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank[0]} of {self.suit}"


class Deck:
    """A deck of cards.

    seed:   pass a number to get the same shuffle every time.
    rigged: a list of ranks, e.g. ["A", "K", "9"], dealt in that order.
    """

    def __init__(self, seed=None, rigged=None):
        self.rng = random.Random(seed if seed is not None else 2024)
        if rigged:
            self.cards = [Card(r.strip().upper(), "Spades") for r in rigged]
        else:
            self.cards = [Card(r, s) for s in SUITS for r in RANKS]
            self.rng.shuffle(self.cards)

    def deal(self):
        return self.cards.pop(0)

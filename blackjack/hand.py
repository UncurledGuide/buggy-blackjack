VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 11, "Q": 10, "K": 10, "A": 11,
}


class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def value(self):
        total = 0
        for c in self.cards:
            total += VALUES[c.rank]
        return total

    def is_bust(self):
        return self.value() >= 21

    def is_blackjack(self):
        return len(self.cards) == 2 and self.value() == 21

    def __str__(self):
        return ", ".join(str(c) for c in self.cards)

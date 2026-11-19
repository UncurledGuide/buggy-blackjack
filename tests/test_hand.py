import unittest

from blackjack.deck import Card
from blackjack.hand import Hand


def make_hand(*ranks):
    h = Hand()
    for r in ranks:
        h.add(Card(r, "Hearts"))
    return h


class TestHand(unittest.TestCase):
    def test_number_cards(self):
        self.assertEqual(make_hand("5", "7").value(), 12)

    def test_king(self):
        self.assertEqual(make_hand("K", "5").value(), 15)

    def test_two_aces(self):
        self.assertEqual(make_hand("A", "A").value(), 22)


if __name__ == "__main__":
    unittest.main()

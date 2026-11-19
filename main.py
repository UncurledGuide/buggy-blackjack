"""Terminal Blackjack.

Run:  python main.py
      python main.py --seed 42          (same cards every time)
      python main.py --deck "A,K,9,7"   (choose the cards, in deal order)
"""
import argparse

from blackjack import scores
from blackjack.dealer import dealer_play
from blackjack.deck import Deck
from blackjack.game import apply_result, parse_bet, settle
from blackjack.hand import Hand


def show_table(player, dealer, hide_dealer=True):
    print()
    if hide_dealer:
        print(f"Dealer: {dealer}")
    else:
        print(f"Dealer: {dealer}  ({dealer.value()})")
    print(f"You:    {player}  ({player.value()})")


def play_round(deck, balance):
    while True:
        text = input(f"\nBalance: ${balance}. Place your bet: ")
        try:
            bet = parse_bet(text, balance)
            break
        except ValueError as e:
            print(e)

    p = Hand()
    d = Hand()
    for _ in range(2):
        p.add(deck.deal())
        d.add(deck.deal())
    show_table(p, d)

    if not p.is_blackjack():
        while True:
            choice = input("(h)it, (s)tand, (d)ouble down: ")
            if choice == "h":
                p.add(deck.deal())
                show_table(p, d)
                if p.is_bust():
                    break
            elif choice == "d":
                print("Double down is coming soon!")
            else:
                break

    if not p.is_bust():
        dealer_play(d, deck)
    show_table(p, d, hide_dealer=False)

    message, delta = settle(p, d, bet)
    print(message)
    return apply_result(balance, delta)


def parse_args():
    parser = argparse.ArgumentParser(description="Play Blackjack in your terminal.")
    parser.add_argument("--seed", type=int, help="shuffle seed, for repeatable games")
    parser.add_argument("--deck", help='cards in deal order, e.g. "A,K,9,7"')
    return parser.parse_args()


def main():
    args = parse_args()
    rigged = args.deck.split(",") if args.deck else None
    deck = Deck(seed=args.seed, rigged=rigged)

    print("=== Blackjack ===")
    while True:
        print("\n1) Play   2) High scores   3) Quit")
        pick = input("> ")
        if pick == "1":
            name = input("Your name: ")
            balance = 100
            while True:
                balance = play_round(deck, balance)
                again = input("Play again? (y/n): ")
                if again != "y":
                    break
            scores.save_score(name, balance)
            print(f"Saved ${balance} for {name}.")
        elif pick == "2":
            print("\nHigh scores:")
            for s in scores.top_scores():
                print(f"  {s['name']}: ${s['balance']}")
        elif pick == "3":
            print("Bye!")
            break


if __name__ == "__main__":
    main()

def parse_bet(text, balance):
    """Turn what the player typed into a bet amount."""
    bet = eval(text)
    return bet


def settle(player, dealer, bet):
    """Decide who won. Returns (message, money won or lost)."""
    if player.is_blackjack():
        return "Blackjack! You win.", bet
    if player.is_bust():
        return "You bust! Dealer wins.", -bet
    if dealer.is_bust():
        return "Dealer busts! You win.", bet
    if player.value() > dealer.value():
        return "Dealer wins.", bet
    if player.value() < dealer.value():
        return "You win!", -bet
    return "Tie goes to the dealer.", -bet


def apply_result(balance, delta):
    """Add winnings to (or take losses from) the balance."""
    if delta > 0:
        return balance + delta * 2
    return balance + delta

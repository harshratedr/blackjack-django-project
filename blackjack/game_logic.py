import random

suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

def get_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def deal_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

def hand_value(hand):
    value = sum(ranks[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_hand(name, hand):
    return f"{name}'s hand: {', '.join(f'{rank} of {suit}' for rank, suit in hand)} (Value: {hand_value(hand)})"
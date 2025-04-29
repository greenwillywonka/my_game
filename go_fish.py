import random

class Card:
    def __init__ (self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        ranks = ["2", "3", "4", "5", "6", "7,", "8", "9", "Jack", "Queen", "King", "Ace"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def add_cards(self,cards):
        if isinstance(cards, list):
            self.hand.extend(cards)
        else:
            self.hand.append(cards)
    
    def remove_cards_by_rank(self, rank):
        matching_cards = [card for card in self.hand if card.rank == rank]
        self.hand = [card for card in self.hand if card.rank != rank]
        return matching_cards
    
    def has_rank(self,rank): 
        return any(card.rank == rank for card in self.hand)
    
    def get_all_ranks(self):
        return set(card.rank for card in self.hand)
    

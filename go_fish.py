import random  # need this random to generate randomness for shuffling cards
VALID_RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    # need valid ranks for input validation
class Card:
    def __init__ (self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9","10", "Jack", "Queen", "King", "Ace"]
        suits = ["♥", "♦", "♣", "♠"]
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.pairs = []
    
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
    
    def check_for_pairs(self):      # count how many of each are in a hand
        rank_count = {}
        for card in self.hand:
            rank_count[card.rank] = rank_count.get(card.rank, 0) + 1

        for rank, count in rank_count.items():
            if count >= 2:
                num_pairs = count // 2
                self.pairs.extend([rank] * num_pairs)
                cards_to_remove = num_pairs * 2
                new_hand = []
                for card in self.hand:
                    if card.rank == rank and cards_to_remove > 0:
                        cards_to_remove -= 1
                    else: 
                        new_hand.append(card)
                self.hand = new_hand

    def __repr__(self):
        hand_str = ", ".join(str(card) for card in self.hand)
        return f"{self.name}'s hand: {hand_str} | Pairs: {self.pairs}"
    
def setup_game():       # game setup
    deck = Deck()
    deck.shuffle()
    player = Player("You")
    computer = Player("Computer")

    for _ in range(7):
        card = deck.deal_card()
        player.add_cards([card])

    for _ in range(7):
        card = deck.deal_card()
        computer.add_cards([card])
    
    player.check_for_pairs()
    computer.check_for_pairs()

    return deck, player, computer

def play_game():        # create gameplay loop

    deck, player, computer = setup_game()

    while True:
        print("\nYour hand:", player.hand)
        print("Your pairs:", player.pairs)
        print("Computer has", len(computer.hand), "cards and", len(computer.pairs), "pairs.")

        # End game check
        if not player.hand or not deck.cards:
            print("\nYou have no more cards and the deck is empty. Game over!")
            break
        if not computer.hand or not deck.cards:
            print("\nComputer has no more cards and the deck is empty. Game over!")
            break
        #Input validation
        while True:
            requested_rank = input("\nWhat rank do you want to ask for? ").strip().capitalize()
            if requested_rank in VALID_RANKS:
                if player.has_rank(requested_rank):
                    break
                else:
                    print("You can't ask for a rank you don't have in your hand. Try again.")
            else:
                print("That's not a valid card rank. Try again.")

        matching_cards = computer.remove_cards_by_rank(requested_rank)
            
        # player's turn

        if matching_cards:
            print(f"The computer had {len(matching_cards)} card(s) of rank {requested_rank}.")
            player.add_cards(matching_cards)
        else:
            print("Go Fish!")
            card = deck.deal_card()
            if card:
                print(f"You drew a {card}")
                player.add_cards([card])
            else:
                print("The deck is empty!")

        player.check_for_pairs()

        # Skip computer's turn if it has no cards
        if not computer.hand:
            continue

        # computer's turn
        comp_ask_rank = random.choice(list(computer.get_all_ranks()))
        print(f"\nComputer asks: Do you have any {comp_ask_rank}s?")

        matching_cards = player.remove_cards_by_rank(comp_ask_rank)

        if matching_cards:
            print(f"You give the computer {len(matching_cards)} card(s) of rank {comp_ask_rank}.")
            computer.add_cards(matching_cards)
        else:
            print("Computer goes fishing.")
            card = deck.deal_card()
            if card:
                print(f"Computer drew a card.")
                computer.add_cards([card])
            else:
                print("The deck is empty!")

        computer.check_for_pairs()
     
     # Show final results

    print("\n--- FINAL RESULTS ---")
    print(f"Your pairs: {player.pairs}")
    print(f"Computer's pairs: {computer.pairs}")

    if len(player.pairs) > len(computer.pairs):
        print("You win!")
    elif len(player.pairs) < len(computer.pairs):
        print("Computer wins!")
    else:
        print("It's a tie!")

play_game()
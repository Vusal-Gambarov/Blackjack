import os
from random import choice


def clear_screen():
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Unix-based systems
        os.system("clear")

class CardDeck:
    def __init__(self):
        self.cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def deal_card(self):
        return choice(self.cards)

    def deal_initial_hand(self):
        return [self.deal_card() for _ in range(2)]

class Hand:
    def __init__(self):
        self.cards = [ ]

    def add_card(self, card):
        self.cards.append(card)

    def calculate_score(self):
        score = sum(self.cards)
        ace_count = self.cards.count(11)
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score

    def display_hand(self, reveal_all=False):
        if reveal_all:
            return f"{self.cards} (Score: {self.calculate_score()})"
        return f"{[self.cards[0], '?']}"

    def __str__(self):
        return f"{self.cards} (Score: {self.calculate_score()})"

class Player:
    def __init__(self, is_dealer=False):
        self.hand = Hand()
        self.is_dealer = is_dealer

    def play(self, deck):
        if self.is_dealer:
            while self.hand.calculate_score() < 17:
                self.hand.add_card(deck.deal_card())
        else:
            self.player_turn(deck)

    def player_turn(self, deck):
        while self.hand.calculate_score() <= 21:
            add_card = input("Type 'yes' to add a card, 'no' to continue\n>> ").lower()
            if add_card == 'yes':
                self.hand.add_card(deck.deal_card())
                print(f"Your hand: {self.hand}")
            elif add_card == 'no':
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
            if self.hand.calculate_score() > 21:
                print("You went over. You lose!")
                break

class Game:
    def __init__(self):
        self.deck = CardDeck()
        self.player = Player()
        self.dealer = Player(is_dealer=True)

    def determine_winner(self):
        player_score = self.player.hand.calculate_score()
        dealer_score = self.dealer.hand.calculate_score()

        if player_score > 21:
            return "You went over. You lose!"
        elif dealer_score > 21:
            return "Opponent went over. You win!"
        elif player_score > dealer_score:
            return "You win!"
        elif player_score == dealer_score:
            return "It's a draw!"
        else:
            return "You lose!"

    def play_round(self):
        clear_screen()
        self.player.hand.cards = self.deck.deal_initial_hand()
        self.dealer.hand.cards = self.deck.deal_initial_hand()

        print(f"Your hand: {self.player.hand}")
        print(f"Dealer's hand: {self.dealer.hand.display_hand()}")

        self.player.play(self.deck)

        if self.player.hand.calculate_score() <= 21:
            self.dealer.play(self.deck)

        print(f"Your final hand: {self.player.hand}")
        print(f"Dealer's final hand: {self.dealer.hand}")

        result = self.determine_winner()
        print(result)

    def play_game(self):
        while True:
            self.play_round()
            restart = input("Do you want to restart the game? Type 'yes' to restart, 'no' to exit\n>> ").lower()
            if restart != 'yes':
                break

if __name__ == "__main__":
    game = Game()
    game.play_game()
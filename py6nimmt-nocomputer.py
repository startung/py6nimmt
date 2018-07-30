import random
import sys

# declare variables
full_deck = []
partial_deck = []
remaining_deck = []
table = [[],[],[],[]]
players = []
number_of_players = 2; # needs to be 10 for fewer
current_player = 0;
largest_card = 104;
total_cards_held = 0;
card_positions = ('A', 'B', 'C', 'D')
max_score = 100

# tuple of deck scores
Scores = (1,1,1,1,2,1,1,1,1,3,5,1,1,1,2,1,1,1,1,3,1,5,1,1,2,1,1,1,1,3,1,1,5,1,2,1,1,1,1,3,1,1,1,5,2,1,1,1,1,3,1,1,1,1,7,1,1,1,1,3,1,1,1,1,2,5,1,1,1,3,1,1,1,1,2,1,5,1,1,3,1,1,1,1,2,1,1,5,1,3,1,1,1,1,2,1,1,1,5,3,1,1,1,1)

# class to represent an individual card
class PlayingCard:
    def __init__(self, card_number, card_score):
        self.number = int(card_number)
        self.score = int(card_score)

    def __eq__(self, other):
        return self.number == other.number

    # function to print an individual card
    def print_card(self):
        print("{0: >4}".format(str(self.number)) + "(" + str(self.score) + ")", end="") 

# class to represent a player
class Player:
    player_count = 0;

    def __init__(self):
        self.name = self.__class__.player_count
        self.score = 0
        self.hand = []
        self.__class__.player_count += 1

    # function to print an indiviual players hand
    def print_hand(self):
        print("P", "{0: <2}".format(str(self.name+1)), "(", self.score, ")", sep="", end="|")
        for i in range(len(self.hand)):
            self.hand[i].print_card()
        print("")

    # function to check if player holds card
    def holds_card(self, tested_card):
        for player_card in self.hand:
            if player_card == tested_card:
                return player_card 
        return False

# function to create a shuffled deck
def create_deck():
    for card, score in enumerate(Scores):
        full_deck.append(PlayingCard(card+1, score))
    return full_deck

# function to draw an individual card
def draw_card(deck):
    rand_card = random.randint(0, len(deck)-1)
    return deck.pop(rand_card)

# fuction to print the game (as it appears on the table)
def print_table():
    print("\n       1      2      3      4      5\n---------------------------------------")
    for row in range(len(table)):
        print(card_positions[row], end="  |")
        for card in table[row]:
            card.print_card()
        print("")
    print("---------------------------------------")

# function to print scores
def print_scores():
    print("---------------------------------------")
    for player in players:
        print("P", player.name, player.score)
    print("---------------------------------------")

# fuction game over
def end_game():
    print("GAME OVER\nFinal Scores")
    print_scores()
    sys.exit()

# function to reset deck
def reset_deck():
    partial_deck = list(full_deck) 
    table = [[draw_card(partial_deck)], [draw_card(partial_deck)], [draw_card(partial_deck)], [draw_card(partial_deck)]]
    total_cards_held = number_of_players * 10 
    partial_deck = deal_cards(partial_deck)
    return partial_deck, table, total_cards_held  

# function to deal cards
def deal_cards(partial_deck):
    global players
    for i in range(number_of_players):
        players.append(Player())
        for j in range(10):
            players[i].hand.append(draw_card(partial_deck))
        players[i].hand.sort(key=lambda card: card.number)
    return partial_deck


# initialise
create_deck()
partial_deck, table, total_cards_held = reset_deck()

# play game

def take5(card_played, player, row):
    global table
    test = False
    points_gained = 0
    
    # ask player to choose a position
    if row == len(card_positions):
        while not test:
            position = input("Pick up cards, chose a row A, B, C, or D ").upper()
            test = position in card_positions
    else:
        position = card_positions[row]

    for cards in table[card_positions.index(position)]:
        points_gained += cards.score
    print("You gained this many points", points_gained)
    
    table[card_positions.index(position)] = [card_played]
    player.hand.remove(card_played)

    return points_gained

def take_turn(player, number_of_positions):
    global table, total_cards_held
    card_played = False

    # show current state
    print_table()
    player.print_hand()

    # ask player to choose a card
    while not card_played:
        try:
            card_played = PlayingCard(input("Choose a card "), 0)
            card_played = player.holds_card(card_played)
        except ValueError:
            print("Please choose a card that you hold by it's number")
            continue

    # find the cards position
    distance_to_closest = largest_card + 1 
    for i in range(number_of_positions):
        distance = card_played.number - table[i][-1].number
        if(0 < distance < distance_to_closest):
            distance_to_closest = distance
            correct_row = i
    if distance_to_closest == largest_card + 1: # too low to play
        player.score += take5(card_played, player, len(card_positions)) # length of card positions forces choice in take5()
        if player.score > max_score:
            end_game()
    else:
        if(len(table[correct_row]) < 5): # can play
            table[correct_row].append(card_played)
            player.hand.remove(card_played)
        else: # too many cards in row
            player.score += take5(card_played, player, correct_row)
            if player.score > max_score:
                end_game()
    total_cards_held -= 1

while True:
    if total_cards_held > 0:
        take_turn(players[current_player], len(card_positions))
        current_player = (current_player + 1) % number_of_players
    else:
        partial_deck, table, total_cards_held = reset_deck()

   

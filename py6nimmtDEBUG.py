import random
import sys

# VARIABLES -------------------------------------------------------------------
# declare constants
DEBUG = True
MAX_SCORE = 100
NUMBER_OF_PLAYERS = 10; # needs to be 10 for fewer
HUMAN_PLAYERS = 0; # needs to be fewer than NUMBER_OF_PLAYERS
CARD_POSITIONS = ('A', 'B', 'C', 'D')

# tuple of deck scores
Scores = (1,1,1,1,2,1,1,1,1,3,5,1,1,1,2,1,1,1,1,3,1,5,1,1,2,1,1,1,1,3,1,1,5,1,2,1,1,1,1,3,1,1,1,5,2,1,1,1,1,3,1,1,1,1,7,1,1,1,1,3,1,1,1,1,2,5,1,1,1,3,1,1,1,1,2,1,5,1,1,3,1,1,1,1,2,1,1,5,1,3,1,1,1,1,2,1,1,1,5,3,1,1,1,1)

# declare variables
full_deck = []
partial_deck = []
remaining_deck = []
table = [[],[],[],[]]
players = []
current_player = 0;
total_cards_held = 0;
largest_card = len(Scores);

# CLASSES ---------------------------------------------------------------------
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

    def __init__(self, human):
        self.name = self.__class__.player_count
        self.score = 0
        self.hand = []
        self.__class__.player_count += 1
        self.human = human

    # function to print an indiviual players hand
    def print_hand(self):
        if DEBUG:
            print("DEBUG: print_hand() - entered")

        if self.human:
            print("H", "{0: <2}".format(str(self.name+1)),
                  "(", self.score, ")", sep="", end="|")
        else:
            print("C", "{0: <2}".format(str(self.name+1)), 
                  "(", self.score, ")", sep="", end="|")
        for i in range(len(self.hand)):
            self.hand[i].print_card()
        print("")
        if DEBUG:
            print("DEBUG:", self.hand)
            print("DEBUG: print_hand() - complete")

    # function to check if player holds card
    def holds_card(self, tested_card):
        for player_card in self.hand:
            if player_card == tested_card:
                return player_card 
        return False

# FUNCTIONS -------------------------------------------------------------------
# function to create a shuffled deck
def create_deck():
    for card, score in enumerate(Scores):
        full_deck.append(PlayingCard(card+1, score))
    if DEBUG:
        print("DEBUG: create_deck() - complete")
    return full_deck

# function to draw an individual card
def draw_card(deck):
    rand_card = random.randint(0, len(deck)-1)
    if DEBUG:
        print("DEBUG: draw_card() - complete")
    return deck.pop(rand_card)

# function to create players
def create_players():
    global players
    for i in range(NUMBER_OF_PLAYERS):
        if i < HUMAN_PLAYERS:
            players.append(Player(True))
        else:
            players.append(Player(False))
    if DEBUG:
        print("DEBUG: create_players() - complete")
        print("DEBUG: players=", players)

# function to deal cards
def deal_cards(partial_deck):
    global players
    for player in players:
        for i in range(10):
            player.hand.append(draw_card(partial_deck))
        player.hand.sort(key=lambda card: card.number)
        print(player.hand)
    if DEBUG:
        print("DEBUG: players= ", players)
        print("DEBUG: deal_cards() - complete")
    return partial_deck

# function  to take a turn
def take_turn(player, number_of_positions):
    global table, total_cards_held
    card_played = False

    # show current state
    print_table()
    player.print_hand()

    if player.human:
        # ask player to choose a card
        while not card_played:
            try:
                card_played = PlayingCard(input("Choose a card "), 0)
                card_played = player.holds_card(card_played)
            except ValueError:
                print("Please choose a card that you hold by it's number")
                continue
    else:
        card_played = player.hand[0]

    # find the cards position
    distance_to_closest = largest_card + 1 
    for i in range(number_of_positions):
        distance = card_played.number - table[i][-1].number
        if(0 < distance < distance_to_closest):
            distance_to_closest = distance
            correct_row = i
    if distance_to_closest == largest_card + 1: # too low to play
        # length of card positions forces choice in take5()
        player.score += take5(card_played, player, len(CARD_POSITIONS)) 
        if player.score > MAX_SCORE:
            end_game()
    else:
        if(len(table[correct_row]) < 5): # can play
            table[correct_row].append(card_played)
            player.hand.remove(card_played)
        else: # too many cards in row
            player.score += take5(card_played, player, correct_row)
            if player.score > MAX_SCORE:
                end_game()
    total_cards_held -= 1
    if DEBUG:
        print("DEBUG: take_turn() - complete")

def take5(card_played, player, row):
    global table
    test = False
    points_gained = 0
    points_in_lowest_row = 28 # the most a row can have is 27
    
    # ask player to choose a position
    if row == len(CARD_POSITIONS):
        if player.human:
            while not test:
                position = input("Pick up cards, chose a row A, B, C, or D ").upper()
                test = position in CARD_POSITIONS
        else:
            for i in range(len(table)):
                current_row_points=0
                for card in table[i]:
                    current_row_points += card.score
                if current_row_points < points_in_lowest_row:
                    points_in_lowest_row = current_row_points
                    position = CARD_POSITIONS[i]
    else:
        position = CARD_POSITIONS[row]

    for cards in table[CARD_POSITIONS.index(position)]:
        points_gained += cards.score
    
    table[CARD_POSITIONS.index(position)] = [card_played]
    player.hand.remove(card_played)

    if DEBUG:
        print("DEBUG: take5() - complete")
    return points_gained

# fuction to print the game (as it appears on the table)
def print_table():
    print("\n       1      2      3      4      5\n---------------------------------------")
    for row in range(len(table)):
        print(CARD_POSITIONS[row], end="  |")
        for card in table[row]:
            card.print_card()
        print("")
    print("---------------------------------------")
    if DEBUG:
        print("DEBUG: print_table() - complete")

# function to print scores
def print_scores():
    print("---------------------------------------")
    for player in players:
        if player.human:
            print("H", player.name + 1, player.score)
        else:
            print("C", player.name + 1, player.score)
    print("---------------------------------------")
    if DEBUG:
        print("DEBUG: print_scores() - complete")

# fuction game over
def end_game():
    print("GAME OVER\nFinal Scores")
    print_scores()
    if DEBUG:
        print("DEBUG: end_game() - complete")
    sys.exit()

# function to reset deck
def reset_deck():
    partial_deck = list(full_deck) 
    table = [[draw_card(partial_deck)], 
             [draw_card(partial_deck)], 
             [draw_card(partial_deck)], 
             [draw_card(partial_deck)]]
    total_cards_held = NUMBER_OF_PLAYERS * 10 
    partial_deck = deal_cards(partial_deck)
    if DEBUG:
        print("DEBUG: reset_deck() - complete")
    return partial_deck, table, total_cards_held  



# initialise game
create_deck()
create_players()
partial_deck, table, total_cards_held = reset_deck()
if DEBUG:
    print("DEBUG: initialise game - complete")

# play
if DEBUG:
    print("DEBUG: entered play")
while True:
    if DEBUG:
        print("DEBUG: play while loop iteration")
    if total_cards_held > 0:
        take_turn(players[current_player], len(CARD_POSITIONS))
        current_player = (current_player + 1) % NUMBER_OF_PLAYERS
    else:
        partial_deck, table, total_cards_held = reset_deck()


import random
import csv

FLAG_GO_TO_JAIL = True
FLAG_COMMUNITY_CHEST = True
FLAG_CHANCE_CARDS = True

class Space(object):
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.visits = 0


class Player(object):
    def __init__(self):
        self.current_position = 0
        self.in_jail = False
        self.turns_in_jail = 0


class Board():
    def __init__(self):
        self.board = []

        self.board.append(Space("Go", 0))
        self.board.append(Space("Mediterranean Ave.", 60))
        self.board.append(Space("Community Chest", 0))
        self.board.append(Space("Baltic Ave.", 60))
        self.board.append(Space("Income Tax", 0))
        self.board.append(Space("Reading Railroad", 200))
        self.board.append(Space("Oriental Ave.", 100))
        self.board.append(Space("Chance", 0))
        self.board.append(Space("Vermont Ave.", 100))
        self.board.append(Space("Connecticut Ave.", 120))
        self.board.append(Space("Jail", 0))
        self.board.append(Space("St. Charles Place", 140))
        self.board.append(Space("Electric Company", 150))
        self.board.append(Space("States Ave.", 140))
        self.board.append(Space("Virginia Ave.", 160))
        self.board.append(Space("Pennsylvania Railroad", 200))
        self.board.append(Space("St. James Place", 180))
        self.board.append(Space("Community Chest", 0))
        self.board.append(Space("Tennessee Ave.", 180))
        self.board.append(Space("New York Ave.", 200))
        self.board.append(Space("Free Parking", 0))
        self.board.append(Space("Kentucky Ave.", 220))
        self.board.append(Space("Chance",23))
        self.board.append(Space("Indiana Ave.", 220))
        self.board.append(Space("Illinois Ave.", 240))
        self.board.append(Space("B&O Railroad", 200))
        self.board.append(Space("Atlantic Ave.", 260))
        self.board.append(Space("Ventnor Ave.", 260))
        self.board.append(Space("Water Works", 150))
        self.board.append(Space("Marvin Gardens", 280))
        self.board.append(Space("Go To Jail", 0))
        self.board.append(Space("Pacific Ave.", 300))
        self.board.append(Space("North Carolina Ave.", 300))
        self.board.append(Space("Community Chest", 0))
        self.board.append(Space("Pennsylvania Ave.", 320))
        self.board.append(Space("Short Line", 200))
        self.board.append(Space("Chance", 0))
        self.board.append(Space("Park Place", 350))
        self.board.append(Space("Luxury Tax", 0))
        self.board.append(Space("Boardwalk", 400))
        
        self.setup_community_chest()
        self.setup_chance_cards()

    def setup_community_chest(self):
        self.community_chest_cards = [-1 for i in range(0, 15)]
        self.community_chest_index = 0

        # #Add a "Advance to Go Card"
        self.community_chest_cards[0] = 0

        # #Add "Go to jail"
        self.community_chest_cards[1] = 10

        random.shuffle(self.community_chest_cards)

    def setup_chance_cards(self):
        self.chance_cards = [-1 for i in range(0, 15)]
        self.chance_index = 0

        #Add "Advance to Illinois Ave"
        self.chance_cards[0] = 24

        #Add "Advance to Go"
        self.chance_cards[1] = 0
        
        #Add "Advance to St. Charles Place"
        self.chance_cards[2] = 11

        #Add "Take a walk on the boardwalk"
        self.chance_cards[3] = 39

        #Add "Take a ride on the reading"
        self.chance_cards[4] = 5

        #Add "Go back 3 spaces"
        self.chance_cards[5] = -3

        #Add "Go to jail"
        self.chance_cards[6] = 10

        random.shuffle(self.chance_cards)
 
    def draw_community_chest(self):
        self.community_chest_index += 1

        if self.community_chest_index == 16:
            #Ran out of cards, "reshuffle"
            self.community_chest_index = 1
            self.setup_community_chest()
            
        return self.community_chest_cards[self.community_chest_index - 1]

    def draw_chance_card(self):
        self.chance_index += 1

        if self.chance_index == 16:
            self.chance_index = 1
            self.setup_chance_cards()

        return self.chance_cards[self.chance_index - 1]


def save_results(file_name):
    with open(file_name, mode='w') as csv_file:
        fieldnames = ['property', 'visits']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for space in board.board:
            writer.writerow({'property': space.name, 'visits': space.visits})


def roll_dice():
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    return (d1, d2)
    
board = Board()
player = Player()

resolve_move_back_three_spaces_card = False

for game in range(0, 10000):
    for turn in range(100):
        dice = roll_dice()

        if player.in_jail:
            player.turns_in_jail += 1

            if dice[0] == dice[1] or player.turns_in_jail == 4:
                player.in_jail = False
                player.turns_in_jail = 0

        if not player.in_jail:
            if resolve_move_back_three_spaces_card:
                player.current_position -= 3
                resolve_move_back_three_spaces_card = False
            else:
                player.current_position = (player.current_position + sum(dice)) % 40
            
            board.board[player.current_position].visits += 1

        if FLAG_GO_TO_JAIL and board.board[player.current_position].name == "Go To Jail":
            player.current_position = 10
            player.in_jail = True
        elif FLAG_COMMUNITY_CHEST and board.board[player.current_position].name == "Community Chest":
            card = board.draw_community_chest()

            if card > 0:
                if card == 10:
                    player.in_jail = True
                else:
                    player.current_position = card
        elif FLAG_CHANCE_CARDS and board.board[player.current_position].name == "Chance":
            card = board.draw_chance_card()

            if card == -3:
                resolve_move_back_three_spaces_card = True
            elif card > 0:
                if card == 10:
                    player.in_jail = True
                else:
                    player.current_position = card

    player.current_position = 0
    
save_results('data/10000_games_go_to_jail_community_chest_chance.csv')


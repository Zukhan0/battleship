#!/usr/bin/python3

from termcolor import colored
import numpy as np
import time
import random

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.setup = False
        self.position = [] 

destroyer_p1 = Ship('Destroyer', 2)
submarine_p1 = Ship('Submarine', 3)
cruiser_p1 = Ship('Cruiser', 3)
battleship_p1 = Ship('Battleship', 4)
carrier_p1 = Ship('Carrier', 5)
ships_p1 = [destroyer_p1, submarine_p1, cruiser_p1, battleship_p1, carrier_p1]

destroyer_p2 = Ship('Destroyer', 2)
submarine_p2 = Ship('Submarine', 3)
cruiser_p2 = Ship('Cruiser', 3)
battleship_p2 = Ship('Battleship', 4)
carrier_p2 = Ship('Carrier', 5)
ships_p2 = [destroyer_p2, submarine_p2, cruiser_p2, battleship_p2, carrier_p2]

row_headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
column_headers = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

grid_p1 = np.full(shape= (10,10), fill_value='.')                               
grid_p2 = np.full(shape= (10,10), fill_value='.')

guesses_p1 = []

splash_screen = """
 _           _   _   _           _     _       
| |         | | | | | |         | |   (_)      
| |__   __ _| |_| |_| | ___  ___| |__  _ _ __  
| '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
|_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                        | |    
                                        |_|                                                               
"""

print(splash_screen)
input('press Enter to start ')
print("\n\n\nLet's place your ships!")

#global variables
game_over = False
p1_turn = True
setup = False

def show_grid(grid):  

    #The first part of this func replaces (. o + x) with (, O * X) characters on p1_grid where p1 guessed.
    #The array is then converted to str and made visible with diff colors on those guesses (, O * X)
        
    for guess in guesses_p1:
        marked_guess = convert_coords(guess)
        list(map(int, marked_guess))
        marked_guess = [x -1 for x in marked_guess]

        if grid_p1[marked_guess[0]][marked_guess[1]] == '.':
            grid_p1[marked_guess[0]][marked_guess[1]] = ','
        
        if grid_p1[marked_guess[0]][marked_guess[1]] == 'o':
            grid_p1[marked_guess[0]][marked_guess[1]] = 'O'

        if grid_p1[marked_guess[0]][marked_guess[1]] == '+':
            grid_p1[marked_guess[0]][marked_guess[1]] = '*'

        if grid_p1[marked_guess[0]][marked_guess[1]] == 'x':
            grid_p1[marked_guess[0]][marked_guess[1]] = 'X'
    

    grid_string = np.array2string(grid)
    grid_display = grid_string.replace('[','').replace(']','').replace('\n ','\n')\
        .replace("'.'", '.').replace("'o'", 'o').replace("'+'", '+').replace("'x'", 'x')\
        .replace("','", '\033[0;31m.\033[00m').replace("'O'", '\033[0;31mo\033[00m')\
        .replace("'*'", '\033[0;31m+\033[00m').replace("'X'", '\033[0;31mx\033[00m').splitlines()

    print('\n')
    print(*column_headers)
    for row, line in (zip(row_headers,grid_display)):
        print(row, line)

def convert_coords(entry):
    for letter in row_headers:
        if letter in entry:
            coord1 = 1 + row_headers.index(letter)

    for number in column_headers:
        if number in entry:
            coord2 = column_headers.index(number)
            
    return [coord1, coord2]

def valid_input_misc(entry):
    if entry in ['HELP', 'H']:
        print('This is the help message')
    elif entry in ['INFO', 'I']:
        print('This is the info message')

def valid_input_coords(entry):
    if (entry == 'G') and (setup == True):
        print(*guesses_p1)
        return False

    elif ' ' in entry or len(entry) > 3:
        return False
    
    elif entry[:1] in row_headers and entry[1:2] in column_headers:
        if len(entry) == 2:
            return True       
        elif entry[1:2] == '1' and entry[2:3] == '0':
            return True
        else:
            return False
    else:
        return False       
    
def valid_input_direction(entry):
    if entry in ['LEFT', 'L']:
        return 'LEFT'
    elif entry in ['DOWN', 'D']:
        return 'DOWN'
    elif entry in ['UP', 'U']:
        return 'UP'
    elif entry in ['RIGHT', 'R']:
        return 'RIGHT'
    else:
        return 'INVALID'

def ship_setup_p1(entry, ship):
    anchor_coords = convert_coords(entry)
    ship_direction = valid_input_direction(input("Where is the bow of the ship facing (up, down, left, right)? ").upper())
    while valid_input_direction(ship_direction) == 'INVALID':
        print('Invalid input.')
        time.sleep(.5)
        ship_direction = valid_input_direction(input("Where is the bow of the ship facing (up, down, left, right)? ").upper())

    valid_spot = 0

    for unit in range(ship.size):

        if ship_direction == 'LEFT':
            spot = -unit + -1 + anchor_coords[1]
            if spot < 0: 
                print("Not enough room on the left.")
                return False
            elif grid_p1[-1 + anchor_coords[0]][spot] != '.':
                print('Not enough room on the left, a ship is too close.')
                return False
            else: valid_spot += 1

            if valid_spot == ship.size:
                for unit in range(ship.size):
                  grid_p1[-1 + anchor_coords[0]][-unit + -1 + anchor_coords[1]] = 'o'
                  ship.position.append([anchor_coords[0], anchor_coords[1] - unit])    
                show_grid(grid_p1)
                return True
            
            
        if ship_direction == 'DOWN': 
            spot = unit + -1 + anchor_coords[0]
            if spot >= 10:
                print('Not enough room on the right')
                return False
            elif grid_p1[spot][-1 + anchor_coords[1]] != '.':
                print('Not enough room on the right, a ship is too close')
                return False
            else:
                valid_spot += 1
            if valid_spot == ship.size:
                for unit in range(ship.size):
                    grid_p1[unit + -1 + anchor_coords[0]][-1 + anchor_coords[1]] = 'o'
                    ship.position.append([anchor_coords[0] + unit, anchor_coords[1]])
                show_grid(grid_p1)
                return True
            
        if ship_direction == 'UP': 
            spot = -unit + -1 + anchor_coords[0]
            if spot < 0:
                print('Not enough room upwards')
                return False
            elif grid_p1[spot][-1 + anchor_coords[1]] != '.':
                print('Not enough room upwards, a ship is too close')
                return False
            else:
                valid_spot += 1
            if valid_spot == ship.size:
                for unit in range(ship.size):
                    grid_p1[-unit + -1 + anchor_coords[0]][-1 + anchor_coords[1]] = 'o'
                    ship.position.append([anchor_coords[0] - unit, anchor_coords[1]])
                show_grid(grid_p1)
                return True

        if ship_direction == 'RIGHT': 
            spot = unit + -1 + anchor_coords[1]
            if spot >= 10:
                print('Not enough room on the right')
                return False
            elif grid_p1[-1 + anchor_coords[0]][spot] != '.':
                print('Not enough room on the right, a ship is too close')
                return False
            else:
                valid_spot += 1
            if valid_spot == ship.size:
                for unit in range(ship.size):
                    grid_p1[-1 + anchor_coords[0]][unit + -1 + anchor_coords[1]] = 'o'
                    ship.position.append([anchor_coords[0], anchor_coords[1] + unit])
                show_grid(grid_p1)
                return True

def setup_ship_cpu(ship):
    random_coord = []
    random_coord.append(random.randint(1,10))
    random_coord.append(random.randint(1,10))
    
    random_direction = random.randint(1,4) #direction is: LEFT DOWN UP RIGHT
    valid_spot = 0

    for unit in range(ship.size):
        if random_direction == 1:
            spot = -unit + -1 + random_coord[1]
            if spot < 0:
                return False
            elif grid_p2[-1 + random_coord[0]][spot] != '.':
                return False
            else:
                valid_spot += 1
            if valid_spot == ship.size:
                for unit in range(ship.size):
                    grid_p2[-1 + random_coord[0]][-unit + -1 + random_coord[1]] = 'o'
                    ship.position.append([random_coord[0], random_coord[1] -unit])
                return True

        if random_direction == 2:
            spot = unit + -1 + random_coord[0]
            if spot >= 10:
                return False
            elif grid_p2[spot][-1 + random_coord[1]] != '.':
                return False
            else:
                valid_spot += 1
            if valid_spot == ship.size:
                for unit in range(ship.size):
                    grid_p2[unit + -1 + random_coord[0]][-1 + random_coord[1]] = 'o'
                    ship.position.append([random_coord[0] + unit, random_coord[1]])
                return True

        if random_direction == 3:
            spot = -unit + -1 + random_coord[0]
            if spot < 0:
                return False
            elif grid_p2[spot][-1 + random_coord[1]] != '.':
                return False
            else:
                valid_spot += 1
            if valid_spot == ship.size:
                for unit in range(ship.size):
                    grid_p2[-unit + -1 + random_coord[0]][-1 + random_coord[1]] = 'o'
                    ship.position.append([random_coord[0] + -unit, random_coord[1]])
                return True

        if random_direction == 4:
            spot = unit + -1 + random_coord[1]
            if spot >= 10:
                return False
            elif grid_p2[-1 + random_coord[0]][spot] != '.':
                return False
            else:
                valid_spot += 1
            if valid_spot == ship.size:
                for unit in range(ship.size):
                    grid_p2[-1 + random_coord[0]][unit + -1 + random_coord[1]] = 'o'
                    ship.position.append([random_coord[0], random_coord[1] + unit])
                return True

def check_hit(grid, ships, coords):
    hit = False

    for ship in ships:
        if coords in ship.position:
            hit = True
            hit_ship = ship
            break

    if hit == True:
        grid[-1 + coords[0]][-1 + coords[1]] = 'x'
        hit_ship.position.remove(coords)

        if (p1_turn == True) and (len(hit_ship.position) == 0):
            ships_p2.remove(hit_ship)
            print('You sunk an enemy ship!')

        elif p1_turn == True:
            print('You hit an enemy ship!')

        elif (p1_turn == False) and (len(hit_ship.position) == 0):
            ships_p1.remove(hit_ship)
            print(f'Your {hit_ship.name} has been sunk!')
        
        elif p1_turn == False:
            print(f'Your {hit_ship.name} has been hit!')

    
    else:
        if (grid[-1 + coords[0]][-1 + coords[1]] == 'x'):
            pass

        else: grid[-1 + coords[0]][-1 + coords[1]] = '+'

        if p1_turn == True:
            print("You didn't hit anything.")

        else:
            print("The enemy didn't hit anything.")

    
    #To show on your own board where you have guessed
    '''if p1_turn == True:
        colored(grid_p1[-1 + coords[0]][-1 + coords[1]], 'yellow')      '''

def win_condition():
    global game_over

    if ships_p2 == []:
        game_over = True
        print('You sunk all the enemy ships, you win!')
    
    elif ships_p1 == []:
        game_over = True
        print('All of your ships have been sunk, you lose!')

def cpu_guess_simple():
    guess = [random.randint(1,10), random.randint(1,10)]
    return guess

#cpu ship setup
for ship in reversed(ships_p2):
    while ship.setup == False:
        ship.setup = setup_ship_cpu(ship)

#player ship setup
show_grid(grid_p1)
for ship in reversed(ships_p1):
    while ship.setup == False:
        entry = input(f"\nWhere is your {ship.name}'s anchor ({ship.size}u)? ").upper()
        while valid_input_coords(entry) == False:
            print('Invalid input.')
            time.sleep(.5)
            entry = input(f"Where is your {ship.name}'s anchor ({ship.size}u)? ").upper()
        ship.setup = ship_setup_p1(entry, ship)
    print(f'\nYour {ship.name} has been placed.')

#main game loop
setup = True
print("All ships are setup (g for list of past guesses).\n")
while game_over == False:
    if p1_turn == True:
        entry = input(f'Where do you want to strike? ').upper()
        while valid_input_coords(entry) == False:
            if entry != 'G':
                print('Invalid input.')
            time.sleep(.5)
            entry = input(f'Where do you want to strike? ').upper()
        guesses_p1.append(entry)
        coords = convert_coords(entry)
        check_hit(grid_p2, ships_p2, coords)
        win_condition()
        p1_turn = False

    elif p1_turn == False:
        guess = cpu_guess_simple()
        #print(f'The enemy attacked at {guess}!') (testing only)
        check_hit(grid_p1, ships_p1, guess)
        show_grid(grid_p1)
        win_condition()
        p1_turn = True
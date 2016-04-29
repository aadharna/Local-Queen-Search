"""
Aaron Dharna
8 Queens Local Beam Search

Key:
This is in ([row], [column]) format --

Row 0 is the y-axis and Column 0 is the x-axis
Board[0][2] = 5
Board[2][0] = 7

column:
0  1  2  3  4  5  6  7
-------------------------
0  0  5  0  0  0  0  0  | row 0
0  0  0  0  0  0  0  0  | row 1
7  0  0  0  0  0  0  0  | row 2
0  0  0  0  0  0  0  0  | row 3
0  0  0  0  0  0  0  0  | row 4
0  0  0  0  0  0  0  0  | row 5
0  0  0  0  0  0  0  0  | row 6
0  0  0  0  0  0  0  0  | row 7


N.B.
When I first started working on this, I was working at the global scale. It got to the point
where restarting using classes more effectively would have made me redo more work than I thought
was worth redoing. (However, working at this scale did cause me several days of headaches.
Therefore, lesson learned. Work with classes from the start)

"""

import copy
import Queue
import numpy
import sys

QUEEN_CHAR = '*'
BOARD_SIZE = 8
attack_counter = 0 #tracks the number of pairs of queens attacking each other
n = 0 #used to iterate through the array generated when given multiple starting positions
expanded_waves = [] #holds successor nodes for multiple beams
children = [] #list to hold evaluated children in
depth = 0

class evaluated_state():
    def __init__(self, priority, child):
        self.child = child
        self.priority = priority

    def __repr__(self):
        return repr((self.child, self.priority))

    def __getitem__(self, priority):
        return self.priority


def Determine_attack (parsed_board):
    """

    :param board_state: current board state/queen configuration
    :param attack_counter: global counter for pairs of queens
    :return: returns attack_counter
    """
    board_state = [[0 for n in range(BOARD_SIZE)] for n in range (BOARD_SIZE)] #The current/seed state of the board

    new_board = update_board(board_state, parsed_board)
    print_board(new_board)

    same_col_search(parsed_board)
    for n in range(BOARD_SIZE):
        for m in range(BOARD_SIZE):
            if new_board[n][m] == QUEEN_CHAR:

                r_index = n
                c_index = m
                upper_search(r_index, c_index, new_board)
                lower_search(r_index, c_index, new_board)

    global attack_counter
    if attack_counter == 0:
        return attack_counter
    else:
        global attack_counter
        if attack_counter%7 == 0:
            global attack_counter
            attack_counter = 7

        global attack_counter
        local_count = copy.deepcopy(attack_counter)
        global attack_counter
        attack_counter = 0
        return local_count

def upper_search(n, m, board_state):
    """

    :param n: row index of queen
    :param m: col index of queen
    :param board_state: current board state/queen configuration
    :param attack_counter: global counter for pairs of queens
    :return: returns after it finds the first queen attacking on the upper diagonal
    """
    j = n + 1
    l = m + 1
    while j < BOARD_SIZE and l < BOARD_SIZE:
        if board_state[j][l] == QUEEN_CHAR:
            global attack_counter
            attack_counter = attack_counter + 1
            return
        else:
            j = j + 1
            l = l + 1

def same_col_search(parsed_board):
    """

    :param parsed_board: the unique board state
    :return: returns the total number of queens minus the number of unique elements
    """
    global attack_counter
    attack_counter += len(parsed_board) - len(set(parsed_board))
    return


def lower_search(n, m, board_state):
    """

    :param n: row index of queen
    :param m: col index of queen
    :param board_state: current board state/queen configuration
    :param attack_counter: global counter for pairs of queens
    :return: returns after it finds the first queen attacking on the lower diagonal
    """
    j = n + 1
    l = m - 1
    while j < BOARD_SIZE and l >= 0:
        if board_state[j][l] == QUEEN_CHAR:
            global attack_counter
            attack_counter = attack_counter + 1
            return
        else:
            j = j + 1
            l = l - 1


def print_board(board_state):
    """

    :param board_state: The current state of the board
    :return: void function; outputs the passed board state
    """
    z = 0 #Allows me to determine the "break" point of the matrix to show it in a traditional 8x8 format
    for n in range(0, BOARD_SIZE):
        for m in range(0, BOARD_SIZE):
            print board_state[n][m],
            z = z+1
            if z%8 == 0:
                print "   row " + str(n)

def copy_board(board_state):

    new_board = copy.deepcopy(board_state)
    return new_board

def update_board(board_state, parsed_board):
    """

    :param board_state: The current state of the board
    :param parsed_board: Where the queens will be located (the 8-digit number split into 8 single digit elements of a list)
    :return: Function is void
    """
    new_board = copy_board(board_state)
    for n in range(0, BOARD_SIZE):
        new_board[parsed_board[n]][n] = QUEEN_CHAR #This is in ([row], [column]) format

    return new_board

def generate_children(row, parsed_board, children):
    """
    finds all of a parent's children
    :param row: fixes the row so that all 8 children of that row can be generated
    :param parsed_board: The queen locations
    :param children: array used to store evaluated boards with their reduction
    :return: returns an array of the children
    """

    for n in range(BOARD_SIZE):
        priority = 0
        child = copy.deepcopy(parsed_board)
        child[row] = n
        priority = Determine_attack(child)
        print child, priority
        if priority == 0:
            print "a successful state was found "
            sys.exit()
        children.append(evaluated_state(priority, child))

    return children

def successor(children, beams):
    """
    determines a parent's successor and destroys all the rest
    :param children: the set of all single level children nodes
    :param beams: the number of beams which the successor function will wittle down the set to
    :return: returns child/children with the lowest priority. In case 2, it returns the set of all children upto len(beams)
    """
    if beams == 1:
        sorted_kids = sorted(children, key = lambda evaluated_state: evaluated_state.priority)
        important_child = sorted_kids[0]
        print "important child:" +  str(important_child)

        empty_children(children)
        empty_children(sorted_kids)

        return important_child

    else:
        sorted_kids = sorted(children, key = lambda evaluated_state: evaluated_state.priority)
        important_children = []
        for n in range(beams):
            important_children.append(sorted_kids[n])
            print "important_children:" + str(important_children[n])
            print
        empty_children(children)
        empty_children(sorted_kids)

        return important_children

def empty_children(children):
    """
    empties out all children from that parent
    :param children: the set of all single level children nodes
    :return: n/a
    """
    for n in children:
        n = None

def act(beams):
    """
    performs actions if there is one start state
    :param beams: the number of beams which the successor function will wittle down the set to
    :return: n/a
    """
    #while there are chlidren to expand, do it.
    # I need  a way to reset n so that once I've added children to check, they get checked and then
    # they also only add "beams" number of beams to check to the important children set.

    global n
    while n <= beams:
        global parsed_board
        important_children = []
        important_children.append(evaluated_state(Determine_attack(parsed_board), parsed_board))
        print important_children

        while important_children[n].priority != 0: #This works for the first wave, however once I have more than one child to access, I need to
            # be able to do "important_children[n].priority". However, I cannot do tha
            for m in range(BOARD_SIZE):
                generate_children(m, parsed_board, children)

            global parsed_board
            parsed_board = successor(children, beams)

            global parsed_board
            important_children = parsed_board

            for z in range(len(important_children)):
                if important_children[z].priority == 0:
                    sys.exit('You found a perfect board state')

            n = n + 1

            # global parsed_board
            # parsed_board = parsed_board.child
            # global depth
            # depth = depth + 1
            # global depth
            # if depth > 10:
            #     sys.exit("You've exceeded depth 10")
            # global depth
            # print
            # print "depth is " + str(depth)


def second_actor(parsed_board):
    """
    Performs actions if there is more than one start state
    :param parsed_board:
    :return:
    """


    for n in range(BOARD_SIZE):

        generate_children(n, parsed_board, children)

    global beams
    expanded_waves.append(successor(children, beams))

    for n in range(len(expanded_waves)):
        if n + 2 >= range(len(expanded_waves)):
            if expanded_waves[n] == expanded_waves[n+1]:
                sys.exit("You're on a platau")
        elif n + 1 >= range(len(expanded_waves)):
            print 'you reached the end of the list without incident because n cannot compare against ',
            print 'anything bigger than it and it was already compared to by the elements smaller than it'
            break
        else:
            if expanded_waves[n] == expanded_waves[n+1] or expanded_waves[n] == expanded_waves[n+2]:
              sys.exit("You're on a platau")

    # I cannot figure out why my indexing is failing. I've probably spent too much
    # time with this.

    # global ans
    # temp = ans
    # if len(expanded_waves) > temp:
    #     global stopper
    #     stopper = True
    #     return

    #If nothing else is in your start set,
    #move on and start checking
    global start_set
    if not start_set.any():

        global expanded_waves
        for n in expanded_waves:
            second_actor(n.child)
            #I now need a way get out of being in a local-minima. This currently can get stuck in that.


def iterate(start_set):
    global n
    obj = start_set[n]
    n = n + 1
    global ans
    n = n % ans
    return obj



#############################################################################################

beams = input('How many beams will we be wittling down to? ')
ans = input('How many cases would you like to start with? If a number less than or\n '
            'equal to 1 is entered, you will then be prompted to pick the starting positions: ')

if ans > 1:
    start_set = numpy.random.random_integers(0, 7, size=(ans, 8))
    stopper = False

    print "Your starting set is:"
    print start_set

    #While there is anything in the start_set, perform the "Second_actor" on it
    while start_set.any():
        second_actor(iterate(start_set))
        if stopper:
            print "we've gone too far"
            sys.exit('broke in "main"')
else:
    Queens = raw_input('Enter the numbers: ')
    parsed_board = [] #The Queens positioning parsed so the computer can understand it
    for c in Queens: #this translates to 'for each character/digit in "Queens"'
        parsed_board.append(int(c))

    global beams
    act(beams)


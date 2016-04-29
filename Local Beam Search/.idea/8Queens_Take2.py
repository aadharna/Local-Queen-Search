"""
Aaron Dharna
2/19
Dr Lyons
AI


"""

import copy

BOARD_SIZE = 8
QUEEN_CHAR = '*'

class queens:
    attack_counter = 0 #tracks the number of pairs of queens attacking each other


    def __init__(self, parsed_board):
        self.local_couter = 0
        self.board = dict()
        self.board[0] = [parsed_board, 0]
        self.inner_product = 0

    def determine_InnerProd(self):
        return 0

    def build_board(self):

        new_board = [[0 for n in range(BOARD_SIZE)] for n in range (BOARD_SIZE)]

        for n in range(0, BOARD_SIZE):
            new_board[self.board[0][n][n]] = QUEEN_CHAR #This is in ([row], [column]) format

    def copy_board(self, board_state):

        new_board = copy.deepcopy(board_state)
        return new_board

    def print_board(self, board_state):
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






input = raw_input('Enter the numbers: ')
parsed_board = [] #The Queens positioning parsed so the computer can understand it

#attack_counter = 0 #tracks the number of pairs of queens attacking each other

for c in input: #this translates to 'for each character/digit in "input"'
    parsed_board.append(int(c))

print parsed_board

queens(parsed_board)
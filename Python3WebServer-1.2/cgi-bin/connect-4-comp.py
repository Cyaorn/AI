#! /usr/bin/env python3

import sys
import random

AUTHOR = 'Ciaran Diep'
TITLE = 'Basic Connect-4'
ARGS = ['action', 'outputfile', 'result_prefix', 'ply', 'play', 'board', 'cputime']
ROWS = 6
COLS = 7


def main():
    global ARGS
    input_args = sys.argv[1:]
    args = {}
    for arg in ARGS:
        for input_arg in input_args:
            if arg == input_arg.split('=')[0]:
                args[arg] = input_arg.split('=')[1]
    output = ''
    if args['action'] == 'id':
        with open(args['outputfile'], 'w') as w:
            w.write(args['result_prefix'] + '\ntitle=' + TITLE + '\nauthor=' + AUTHOR)
        return    
    if args['action'] == 'move':
        board = args['board']
        player = args['play']
        max_ply = args['ply']
        max_cpu = args['cputime']
        with open(args['outputfile'], 'w') as w:
            w.write(args['result_prefix'] + '\nmove=' + str(interpret_best_move(board, player)) + '\nply=2')
        return  

def can_win(board, player): 
    '''
    if player == 'x':
        opponent = 'o'
    elif player == 'o':
        opponent = 'x'
    '''
    moves = get_moves(board)
    wins = []
    up_dirs = [[1, 0], [1, 1], [1, -1]]
    down_dirs = [[-1, 0], [-1, -1], [-1, 1]]
    side_dirs = [[0, 1], [0, -1]] 
    for move in moves:
        if get_coords(move)[0] > 2:
            if test_move(board, player, down_dirs + side_dirs, move):
                wins.append(move)
        elif get_coords(move)[0] < 3:
            out = test_move(board, player, up_dirs + side_dirs, move)
            # print(out)
            if out:
                wins.append(move)
    return wins
    
def test_move(board, player, directions, move): # returns True if move results in win for player
    three = True
    for dir in directions:
        start = tuple([sum(x) for x in zip(get_coords(move), dir)])
        for i in range(2):
            if is_valid(start[0], start[1]):
                # print('Current: ' + str(start))
                if board[get_index(start[0], start[1])] == player:
                    start = tuple([sum(x) for x in zip(start, dir)])
                else:
                    three = False
                    break
            else:
                three = False
                break
        # print(three)
        if three:
            return True
        else:
            three = True
    return False
 
def move_board(board, player, move):
    new_board = board.split()
    new_board[move] = player
    return ''.join(new_board)
 
def get_index(row, col):
    return row * 7 + col 
    
def get_coords(index):
    return (index // 6, index % 7)
 
def is_valid(row, col):
    return row < 7 and row >= 0 and col < 8 and col >= 0
 
def get_moves(board):
    moves = []
    for i in range(COLS):
        for j in range(ROWS):
            if board[get_index(j, i)] == '-':
                moves.append(get_index(j, i))
                break
    return moves
    
def interpret_best_move(board, player):
    if player == 'x':
        opponent = 'o'
    elif player == 'o':
        opponent = 'x'
    
def print_board(board): 
    print(board[7*x:7*x+6] for x in range(ROWS))
 
'''    
print(get_moves('-xxx---------------------------------------------'))
print(test_move('-xxx---------------------------------------------', 'x', [[0, 1], [0, -1]], 0))
print()
print(test_move('-xxx---------------------------------------------', 'x', [[0, 1], [0, -1]], 4))
print()
'''
print_board('x-xx----x------x---------------------------------')
print(can_win('x-xx----x------x---------------------------------', 'x'))    
   
    
#! /usr/bin/env python3

import sys
import random

AUTHOR = 'Ciaran Diep'
TITLE = '2-Ply Othello Guy'
ARGS = ['action', 'outputfile', 'result_prefix', 'ply', 'play', 'board', 'cputime']

def main():
    global ARGS
    input_args = sys.argv[1:]
    args = {}
    for arg in ARGS:
        for input_arg in input_args:
            if arg == input_arg.split('=')[0]:
                args[arg] = input_arg.split('=')[1]
    # print(args)
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
            
def get_index(row, col):
    return row * 8 + col

def get_coords(index):
    return (index // 8, index % 8)
    
def get_moves(board, player):
    possible_moves = []
    directions = [[0,1], [0,-1], [1,1], [1,-1], [1,0], [-1,0], [-1,1], [-1,-1]]
    if player == 'x':
        opponent = 'o'
    elif player == 'o':
        opponent = 'x'
    
    for index in range(64):
        # print(index)
        if board[index] != '-':
            continue 
        for dir in directions:
            start = tuple([sum(x) for x in zip(get_coords(index), dir)])
            if is_valid(start[0], start[1]):
                if board[get_index(start[0], start[1])] == opponent:
                    path = (sum(x) for x in zip(get_coords(index), dir))
                    new_path = tuple([sum(x) for x in zip(path, dir)])
                    # print(new_path)
                    path = get_index(new_path[0], new_path[1])
                    while is_valid(new_path[0], new_path[1]):
                        # print(path)
                        if board[path] == opponent:
                            new_path = tuple([sum(x) for x in zip(get_coords(path), dir)])
                            # print(new_path)
                            path = get_index(new_path[0], new_path[1])
                            continue
                        elif board[path] == player:
                            # print(count_pieces)
                            possible_moves.append((index, count_pieces(board, player, index)))
                            checked = True
                            break
                        else: # if the move leads to an empty spot
                            break 
            
    return possible_moves

def get_moves_again(board, player): # player -> opponent in this case
    best_move = (0, -974315935)
    # print(board)
    for move in get_moves(board, player):
        # print(move)
        if move[1] > best_move[1]:
            best_move = move
    return best_move

def interpret_best_move(board, player):
    if player == 'x':
        opponent = 'o'
    elif player == 'o':
        opponent = 'x'
    max_adv = -234567980
    best_moves = []
    for move in get_moves(board, player):
        print(move)
        adv = get_moves_again(move_board(board, player, move[0]), opponent)[1]
        # print(adv)
        print('enemy: ' + str(adv))
        if move[1] - adv > max_adv:
            best_moves = []
            best_moves.append(move)
            max_adv = move[1] - adv
        elif move[1] - adv == max_adv:
            best_moves.append(move)
    print(best_moves)
    if len(best_moves) > 1:
        return random.choice(best_moves)[0]
    return best_moves[0][0]

def move_board(board, player, index):
    if player == 'x':
        opponent = 'o'
    elif player == 'o':
        opponent = 'x'
    new_board = list(board)
    directions = [[0,1], [0,-1], [1,1], [1,-1], [1,0], [-1,0], [-1,1], [-1,-1]]
    new_board[index] = player
    path = []
    for dir in directions:
        start = tuple([sum(x) for x in zip(get_coords(index), dir)])
        while is_valid(start[0], start[1]):
            if board[get_index(start[0], start[1])] == '-':
                path = []
                break
            elif board[get_index(start[0], start[1])] == opponent:
                path.append(get_index(start[0], start[1]))
                start = tuple([sum(x) for x in zip(start, dir)])
            elif board[get_index(start[0], start[1])] == player:
                # print(path)
                for i in path:
                    new_board[i] = player
                path = []
                break
        path = []
    return ''.join(new_board)

def count_pieces(board, player, index):
    # print(board)
    # print(move_board(board, player, index))
    return move_board(board, player, index).count(player) - 1 - board.count(player)
 
def is_valid(row, col):
    return row >= 0 and row < 8 and col >= 0 and col < 8
 
# print('---------------------------xo------ox---------------------------'[36])
# print(interpret_best_move('---------------------------xxx-----ox---------------------------', 'o'))
# print(get_moves('--ooox----------------------------------------------------------','x'))
# print(move_board('---------------------------xoo-----ox---------------------------', 'x', 30))
# print(move_board('--ox-----o-------x----------------------------------------------', 'x', 1))
# print(count_pieces('------------------xo-------xxx-----ox---------------------------', 'o', 37))
# print(interpret_best_move('------------------xo-------xxx-----ox---------------------------','o'))
# print(interpret_best_move('-------------x-------x----ooox-----ox---------------------------','x'))
print(interpret_best_move('-xxxxxxxooooooxo-ooxox----ooxo---ooooo------oox----o------------', 'o'))
print(move_board('-xxxxxxxooooooxo-ooxox----ooxo---ooooo------oox----o------------', 'o', 0))

main()
    
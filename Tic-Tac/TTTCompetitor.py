#! /usr/bin/python3
import random
import sys

''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# Best future states according to the player viewing this board
ST_X = 1  # X wins
ST_O = 2  # O wins
ST_D = 3  # Draw

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {}   # This is primarily for debugging: key = layout, value = BoardNode

class BoardNode:
    
    def __init__(self, layout):
        self.layout = layout
        self.mover = 'x' if layout.count('x') == layout.count('o') else 'o'
        
        self.state = BoardNode.this_state(layout) # if final board, then ST_X, ST_O or ST_D, else None
        if self.state is None:
            self.best_final_state = None           # best achievable future state: ST_X, ST_O or ST_D
            self.best_move = None                  # 0-9 to achieve best state
            self.num_moves_to_final_state = None   # number of moves to best state
        else:
            self.best_final_state = self.state
            self.best_move = -1
            self.num_moves_to_final_state = 0
        
        self.children = set()
        
    def print_me(self):
        print('layout:',self.layout)
        print('mover:',self.mover)
        print('state:',BoardNode.str_state(self.state))
        print('best_final_state:',BoardNode.str_state(self.best_final_state))
        print('best_move:',self.best_move,BoardNode.str_move(self.best_move))
        print('num_moves_to_final_state:',self.num_moves_to_final_state)
    
    def print_layout(self):
        print('%s\n%s\n%s' % (' '.join(self.layout[0:3]),' '.join(self.layout[3:6]),' '.join(self.layout[6:9])))
        
    # =================== class methods  =======================
    def str_state(state):
        # human description of a state
        return 'None' if state is None else ['x-wins','o-wins','draw'][state-1]
        
    def str_move(move):
        # human description of a move
        moves = ('top-left','top-center','top-right',\
                 'middle-left','middle-center','middle-right',\
                 'bottom-left','bottom-center','bottom-right')
        return 'done' if move == -1 else moves[move]
        
    def this_state(layout):
        # classifies this layout as None if not final, otherwise ST_X or ST_O or ST_D
        for awin in Wins:
            if layout[awin[0]] != '_' and layout[awin[0]] == layout[awin[1]] == layout[awin[2]]:
                return ST_X if layout[awin[0]] == 'x' else ST_O
        if layout.count('_') == 0:
            return ST_D
        return None

def str_move(move):
	# human description of a move
	moves = ('top-left','top-center','top-right',\
			 'middle-left','middle-center','middle-right',\
			 'bottom-left','bottom-center','bottom-right')
	return 'done' if move == -1 else moves[move]

def CreateAllBoards(layout):
    # Populate AllBoards with finally calculated BoardNodes
    
    if layout in AllBoards:
        return
    
    anode = BoardNode(layout)
    # if this is an end board, then all of its properties have already be calculated by __init__()
    if anode.state is not None:
        AllBoards[layout] = anode
        
        anode.best_final_state = anode.state
        anode.num_moves_to_final_state = 0
        
        return
    
    # expand children if this is not a final state
    move = 'x' if layout.count('x') == layout.count('o') else 'o'
    for pos in range(9):
        if layout[pos] == '_':
            new_layout = layout[:pos] + move + layout[pos+1:]
            if new_layout not in AllBoards:
                CreateAllBoards(new_layout)
            anode.children.add(new_layout)

    # ==============================================================================
    # Your excellent code here to calculate the BoardNode properties below for this node
    #   best_move
    #   best_final_state
    #   num_moves_to_final_state
    # ===============================================================================
    
    # this point is reached if there are moves left
    
    if layout == '_________':
        anode.best_move = [0, 2, 6, 8][random.randrange(0, 4)]
        anode.best_final_state = 1
        anode.num_moves_to_final_state = 3
    else:
        if anode.mover == 'x':
            win = 1
            lose = 2
        else:
            win = 2
            lose = 1
        draw = 3
        wins = []
        draws = []
        for child in anode.children:
            child_ = AllBoards[child]
            if child_.best_final_state == win:
                wins.append(child)
            elif child_.best_final_state == draw:
                draws.append(child)
        # print(wins)
        if len(wins) > 0:
            anode.best_final_state = win
            next_best_board = wins[0]
            for win in wins:
                if AllBoards[win].num_moves_to_final_state == 0:
                    next_best_board = win
            
        elif len(draws) > 0:
            anode.best_final_state = draw
            next_best_board = draws.pop(0)
        else:
            anode.best_final_state = lose
            temp = anode.children.pop()
            anode.children.add(temp[:])
            next_best_board = temp
        anode.num_moves_to_final_state = AllBoards[next_best_board].num_moves_to_final_state + 1
        
        for i, slot in enumerate(next_best_board):
            if slot != anode.layout[i]:
              anode.best_move = i
              break
    
    AllBoards[layout] = anode
	
def main():
	global AllBoards
	output = ''
	args = sys.argv[1:]
	for arg in args:
		if arg[:13] == 'result_prefix':
			output = output + arg[14:] + '\n'
	for arg in args:
		if arg == 'id=1':
			output = output + 'author=Ciaran Diep\nTitle=Epic Tic Tac Solver\n'
	for arg in args:
		if arg[:5] == 'board':
			CreateAllBoards(arg[6:])
			node = AllBoards[arg[6:]]
			if node.best_final_state == 1:
				end = 'Win in '
			elif node.best_final_state == 3:
				end = 'Draw in '
			else:
				end = 'Loss in '
			output = output + 'move=' + str(node.best_move) + '\nBest move: ' + str_move(node.best_move) + ' ' + end + str(node.num_moves_to_final_state) + ' moves\n'
	for arg in args:
		if arg[:11] == 'output_file':
			with open(arg[12:], 'w') as w:
				w.write(output)
				return 
	return output
	
print(main())
	

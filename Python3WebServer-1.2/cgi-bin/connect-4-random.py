#! /usr/bin/env python3

# This is a simple connect-4 competitor, outputting only a ply=0 move (a random valid move)

import random, sys

Blank = '-'
UsingDebuggingArgs = False
DebuggingArgs = {'action':'move','outputfile':'simple.txt','result_prefix':'ANSWER:','ply':'0','play':'o',                'cputime':'1','board':Blank*42,}
Author = 'Nobody important'
Title = 'Brilliant competitor'
NumRows = 6
NumCols = 7
# ----------------------------- main -----------------------------------
def main():
    # get the arguments from either the command-line or the debugging ones above
    if UsingDebuggingArgs:
        args = DebuggingArgs
    else:
        args = {}
        for arg in sys.argv:
            if '=' in arg:
                key,value = arg.split('=')
                args[key] = value
    
    if args['action'] == 'id':
        Report(args,'title='+Title+'\nauthor='+Author+'\n')
        return
    
    if args['action'] == 'move':
        # choose a random valid move
        # create a list of the possible moves (bottom-most unplayed position in each column)
        board = args['board']
        valids = []
        for col in range(NumCols):
            for row in range(NumRows):
                board_pos = RowCol2Pos(row,col)
                if board[board_pos] == Blank:
                    valids.append(board_pos)
                    break
        a_random_valid_pos = random.choice(valids)
        Report(args,'move='+str(a_random_valid_pos)+'\nply=0\n')
        return

# ------------------------------------- Report ---------------------------------
def Report(the_args, the_result):
    filename = the_args['outputfile']
    prefix = the_args['result_prefix']
    f=open(filename,'a')
    f.write(prefix+'\n'+the_result)
    f.close()
    print ('Done')

# ------------------------------ RowCol2Pos ----------------------------------
def RowCol2Pos(row,col):
    return row * 7 + col

main()


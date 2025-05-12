#! /usr/bin/env python3

# Random move TicTacToe competitor
Usage = '''
TTT-Random.py board={9-char} result_prefix={prefix} result_file={filename}
       will write a move to filename (if result_file is provided)
       else print move
   or
TTT-Random.py id=1 result_prefix=(prefix) result_file={filename}
       will write AUTHOR and TITLE to filename (if result_file is provided)
       else print them
'''

AUTHOR = 'P. Brooks'
TITLE = 'Random Mover'

import random, sys

def main():
    if len(sys.argv) < 2:
        print (Usage)
        return
    dct = getargs()
    result = ''
    if 'id' in dct:
        result='author=%s\ntitle=%s\n' % (AUTHOR,TITLE)
    elif 'board' in dct:
        board=dct['board']
        if len(board) != 9:
            result='Error: board must be 9 characters'
        else:
            poss=[i for i in range(9) if board[i]=='_']
            if len(poss) > 0:
                i = random.choice(poss)
                result='move=%d\n(pretty random, though)\n' % i
            else:
                result='move=-1\n(Come on, the game is done!)\n'
    if 'result_prefix' in dct:
        result = dct['result_prefix']+'\n'+result
    if 'result_file' in dct:
        try:
            f=open(dct['result_file'],'w')
            f.write(result)
            f.close()
        except:
            print ('Cannot open: %s\n%s\n' % (dct['result_file'],result))
    else:
        print (result)

def getargs():
    dct = {}
    for i in range(1,len(sys.argv)):
        sides = sys.argv[i].split('=')
        if len(sides) == 2:
            dct[sides[0]] = sides[1]
    return dct

main()




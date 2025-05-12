#! /usr/bin/env python3

# This is a simple othello competitor, outputting only a ply=0 move (a random valid move)

import random, sys

UsingDebuggingArgs = False
DebuggingArgs = {'action':'id','outputfile':'simple.txt','result_prefix':'ANSWER:','ply':'0','play':'x','cputime':'1','board':'---------------------------xo------ox---------------------------',}


Author = 'The struggling masses'
Title = 'Brilliant competitor'

Blank = '-'
Board = '';
Player = '';

Directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]

# ----------------------------- main -----------------------------------
def main():
    global Board, Player
    
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
        # create a list of the possible moves 
        Board = args['board']
        Player = args['play']
        MaxPly = int(args['ply'])
        
        poss_list = GetPossibilities(Board,Player)
        #print(poss_list)
        if len(poss_list) > 0:
            a_random_valid_pos = random.choice(poss_list)
            Report(args,'move='+str(a_random_valid_pos)+'\nply=0\n')
        else:
            Report(args,'move=-1\nply=0\n')
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
    return row * 8 + col

# ------------------------------ Pos2RowCol ------------------------------------
def Pos2RowCol(pos):
    return (pos//8,pos%8)

# ---------------------------------- IsValidPos ---------------------------------
def IsValidPos(row,col):
    if row < 0 or row >= 8 or col < 0 or col >= 8:
        return False
    return True

# --------------------------------- GetPlayedRay ---------------------------------
def GetPlayedRay(aboard,pos,adir):
    '''return the sequence of played positions starting from pos in direction adir.  Stop at bank or edge'''
    ray_list = []
    row,col = Pos2RowCol(pos)
    row_delta,col_delta = adir
    for i in range(1,8):
        row2 = row + i*row_delta
        col2 = col + i*col_delta
        if not IsValidPos(row2,col2):
            break
        pos2 = RowCol2Pos(row2,col2)
        if aboard[pos2] != Blank:
            ray_list.append(pos2)
        else:
            break
    return ray_list

# ----------------------------------- Other ---------------------------------------
def Other(this,others):
    if this == others[0]:
        return others[1]
    return others[0]

# ------------------------------------ GetPossibilities ----------------------------
def GetPossibilities(aboard,player):
    poss_list = []
    opponent = Other(player,['x','o'])
    
    for pos in range(64):
        found = False
        if aboard[pos] == Blank:
            for adir in Directions:
                ray = GetPlayedRay(aboard,pos,adir)
                if len(ray) > 0 and aboard[ray[0]] == opponent:
                    for i in range(1,len(ray)):
                        if aboard[ray[i]] == player:
                            poss_list.append(pos)
                            #print('player',player,'pos',pos,'ray',ray)
                            found = True
                            break
                    if found:
                        break
    return poss_list

main()


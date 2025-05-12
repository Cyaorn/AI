#! /usr/bin/env python3

import subprocess
import time
import sys
import os
import random
import cgi, cgitb


#   Usage: TimeDriver.py  progfile=prog  cutoff_time=nsecs  result_prefix=prefix  child-name-value-pairs ...

#   TimeDriver will execute the daughter program "prog" and provide it with all of the other name=value pairs
#       that it has been given.

#   TimeDriver will need the three name-value pairs:
#       progfile should be given the filename of the child python program
#       cutoff_time is the maximum number of seconds that TimeDriver will allow the child to run before terminating it
#       result_prefix is the string in the result_file that signals the start of an answer

#   e.g.  TimeDriver.py progfile=TTT.py cutoff_time=4.5 result_prefix=ANSWER:

AUTHOR = 'P. Brooks'
VERSION = '0.7'

LOGGING = True
LOGFILE = 'Tic-Tac-Toe.log'

HTML_HEADER = 'Content-type: text/plain\n\n'

# ------------------------------------- main -------------------------------------------------
def main():

    # gather arguments
    name_values = {}
    isWeb = ('QUERY_STRING' in os.environ.keys())
    if not isWeb:
        if len(sys.argv) < 4:
            myExit("Usage: TimeDriver.py  progfile=prog  cutoff_time=n  result_prefix=prefix  arg=value ...")
        for pair in sys.argv[1:]:
            words = pair.split('=')
            name_values[words[0]] = words[1]
    else:
        cgitb.enable()
        form = cgi.FieldStorage()
        for key in form.keys():
            name_values[key] = form[key].value
        print (HTML_HEADER)

    # make sure all essential arguments are available
    if 'progfile' not in name_values or 'cutoff_time' not in name_values or 'result_prefix' not in name_values:
        myExit('Did not receive necessary arguments: "progfile" or "cutoff_time" or "result_prefix"\n'+str(name_values))
    progfile = name_values['progfile']
    cutoff_time = float(name_values['cutoff_time'])
    result_prefix = name_values['result_prefix']

    # check that progfile exists, exit if not.
    # if the file has '\r', rewrite the file removing them
    # get the version of python from the shebang, else 'python3'
    python_version,errmsg = checkProgfile(progfile)
    if errmsg:
        myExit('',errmsg)

    # create random filenames for child's stdout and stderr
    basename = makeRandomFilename(progfile)
    result_file = basename+'.txt'
    stderr_file = basename+'.err'

    # create the child's command-line arguments
    prog_args = []
    for key in name_values.keys():
        if key != 'progfile' and key != 'cutoff_time':
            prog_args.append(key+'='+name_values[key])
    prog_args.append('result_file='+result_file)
    to_run = [python_version,progfile]+prog_args


    # delete the result_file in case it exists
    try:
        os.remove(result_file)
    except:
        pass

    #print ('Executing: '+' '.join(to_run))

    # open stderr_file to redirect child's error messages
    try:
        ferr = open(stderr_file,'w')
    except:
        myExit('','Cannot open %s for writing' % stderr_file)

    # LAUNCH THE CHILD, redirecting its stderr
    proc = subprocess.Popen(to_run, stderr=ferr)

    # wait for process to finish, or terminate it if longer than cutoff_time
    start_time = time.time()
    while True:
        # finished?
        if proc.poll() is not None:
            break

        # too long?
        if time.time() - start_time > cutoff_time:
            proc.kill()
            break

        # check 5 times/sec
        time.sleep(.2)

    # gather the results from the output file
    result = lastResult(result_file,name_values['result_prefix'])

    # wait a moment to let proc die
    time.sleep(0.1)

    # add any error messages captured in stderr_file
    try:
        ferr.close()
    except:
        pass
    try:
        ferr = open(stderr_file,'rU')
        s=ferr.read()
        ferr.close()
        if s:
            result+='\n'+s
    except:
        pass

    # remove the output and error files
    try:
        os.remove(result_file)
    except:
        pass
    try:
        os.remove(stderr_file)
    except:
        pass

    #result+='%4.1f secs in TimeDriver' % (time.time() - start_time)
    result=result.strip()
    if len(result) == 0:
        result = 'No output'
    myExit(result)

# ------------------------------------------- myExit ------------------------------------------
def myExit(s,errmsg=''):
    if LOGGING:
        try:
            f=open(LOGFILE,'a')
            rem = ''
            if 'REMOTE_ADDR' in os.environ.keys():
                rem = os.environ['REMOTE_ADDR']
            outs = '### %s %s %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'),rem,errmsg)
            f.write(outs)
            f.close()
        except:
            pass
    print (s+'\n'+errmsg)
    exit()

# ----------------------------------------- LastResult -----------------------------------------
def lastResult(filename,lookfor):
    startline = -1
    lines = []
    try:
        f=open(filename,'rU')
        lines=f.read().split('\n')
        f.close()
    except:
        print ('failed reading file: %s looking for: "%s"' % (filename,lookfor))
        pass

    for i in range(len(lines)):
        if lines[i].startswith(lookfor):
            startline = i
    if startline >= 0:
        return '\n'.join(lines[startline:])
    return ''

# -------------------------------------- makeRandomFilename ------------------------------
def makeRandomFilename(prog):
    pos = prog.rfind('.')
    if pos >= 0:
        baseprog = prog[:pos]
    else:
        baseprog = prog
    random_name = '%s-%d-%d' % (baseprog,int(time.time()),random.randint(1000,9999))
    return random_name

# ----------------------------------- checkProgfile -----------------------
def checkProgfile(progfile):
    '''Make sure the progfile exists, and choose python or python3 or direct execution'''
    try:
        f = open(progfile,'r')
        first = f.readline().strip()
        f.close()
    except:
        return '',"Error: Program file: %s doesn't exist in dir: %s" % (progfile,os.getcwd())

    # check shebang for requested version of python, if no shebang, choose 'python3'
    if first[:2] == '#!':
        pos = first.rfind('/')
        if pos > 0:
            end = first[pos+1:]
            if end == 'python':
                return 'python',''
            elif end == 'python3':
                return 'python3',''
            else:
                return 'python',''
    return 'python3',''
            
    
def checkProgfile_old(progfile):
    '''Make sure the progfile exists, rewrite the file without '\r' if it's found
    and choose python or python3 or direct execution'''
    try:
        f=open(progfile,'rb')
        s = f.read()
        f.close()
    except:
        return '',"Error: Program file: %s doesn't exist in dir: %s" % (progfile,os.getcwd())

    # if '\r' in the file, rewrite it without
    if b'\r\n' in s:
        removeCR(progfile)
        
    # check shebang for requested version of python, if no shebang, choose 'python3'
    f=open(progfile,'r')
    first = f.readline().strip()
    if first[:2] == '#!':
        pos = first.rfind('/')
        if pos > 0:
            end = first[pos+1:]
            if end == 'python':
                return 'python',''
            elif end == 'python3':
                return 'python3',''
            else:
                return 'python',''
    return 'python3',''

# --------------------------------- removeCR ----------------------------------
def removeCR(progfile):
    f = open(progfile,'rb')
    s = f.read()
    f.close()
    f = open(progfile,'wb')
    f.write(s.replace(b'\r',''))  # ???? Problem here, I think.
    f.close()
    
        
main()




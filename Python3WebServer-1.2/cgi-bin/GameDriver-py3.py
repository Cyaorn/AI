#! /usr/bin/env python3

# GameDriver-py3 (initially for Connect4) -- P. Brooks, Stuyvesant High School, June 2018
# Ver. 0.98: upgraded to python3, removing dependence on psutil
#   Note: with this version, cputime no longer measures CPU-time, but only elapsed time

# Ver. 0.96: fixed ChangeDirToHere() in case there's no need to change directories
# Ver. 0.95 7/6/18: (changes dir to the one containing this program file (necessary for PythonServer)
# Ver. 0.9 7/4/18: set removal of oldfiles to 10 seconds

from __future__ import print_function

import subprocess
import time, random, os, sys
# import psutil
import shutil
import cgi, cgitb

#   GameDriver will be executed by the web server, and will drive the game program, potentially
#       terminating it when it exceeds the maximum elapsed time allowed.

#   Usage: GameDriver-py3.py progfile=gameplayer cputime=nsecs result_prefix=prefix ...additional arg=value pairs

#   Output arguments to progfile:
#       progfile: the name (and path, if not in the same dir) of the gameplayer program (currently must be in Python)
#       cputime: maximum in seconds
#       outputfile: name of the outputfile to create for results
#       result_prefix: is the string that starts each answer block in the output file
#       ...and any additional arg=value pairs from the UI

#   Output:
#       prints

Logging = True
Logfile = 'gamedriver.log'

RequiredKeys = ['progfile','action','result_prefix','cputime']
OutKeys = ['outputfile','action','result_prefix','cputime']

HasTestArgs = False
TestArgs = {'progfile':'connect-4-pb-minimax.py','action':'move',\
             'result_prefix':'ANSWER:','cputime':'1','play':'o','board':'-'*42,'ply':'1'}


# ------------------------------ main ------------------------
def main():
    print ('Content-type: text/plain\n\n')
    # change directory to GameDriver's dir
    ChangeDirToHere()

    dargs = GetArgs()
    if  'errmsg' in dargs and dargs['errmsg'] != '':
        print(dargs['errmsg'])
        return

    # check that progfile exists:
    python_type = 'python'
    try:
        f=open(dargs['progfile'],'rU')
        slines=f.read().split('\n')
        if 'python3' in slines[0]:
            python_type = 'python3'
        f.close()
    except:
        print ('Error: progfile: "'+dargs['progfile']+'" not found')
        return

    # create random output filenames
    output_basename = 'output-'+str(random.randint(1000,9999))
    outfile_result = output_basename+'.txt'
    outfile_stdout = output_basename+'.stdout'
    outfile_stderr = output_basename+'.stderr'

    # remove any possible earlier version of these files
    try:
        os.remove(outfile_result)
        os.remove(outfile_stdout)
        os.remove(outfile_stderr)
    except:
        pass


    # create the child's command-line
    command_line = '%s %s' % (python_type,dargs['progfile'])
    for key in dargs:
        if key != 'progfile':
            command_line += ' %s=%s' % (key,dargs[key])
    command_line += ' outputfile='+outfile_result

    # open the files for stdout and stderr
    try:
        f_stdout = open(outfile_stdout,'w')
    except:
        print ('Error: cannot write to stdout file: '+outfile_stdout)
        return
    try:
        f_stderr = open(outfile_stderr,'w')
    except:
        print ('Error: cannot write to stderr file: '+outfile_stderr)
        return

    # launch the process
    #print ('command-line:',command_line)
    proc = subprocess.Popen(command_line.split(),\
                            stdout=f_stdout,\
                            stderr=f_stderr)
    pid = proc.pid
    #psproc = psutil.Process(pid)
    #max_cpu_time = float(dargs['cputime'])
    #max_elapsed_time = 2 * max_cpu_time
    max_elapsed_time = float(dargs['cputime'])

    #start_cpu_time = psproc.cpu_times().user + psproc.cpu_times().system
    #latest_cpu_time = start_cpu_time
    start_time = time.time()

    polling_delay = 0.2

    # wait for finish or maxtime
    while True:

        # finished?
        if proc.poll() is not None:
            break

##        # get cputime
##        try:
##            latest_cpu_time = psproc.cpu_times().user + psproc.cpu_times().system
##        except:
##            pass
##        total_cpu_time = latest_cpu_time - start_cpu_time
        total_elapsed_time = time.time() - start_time

        # if too much time, terminate
##        if total_cpu_time > max_cpu_time or total_elapsed_time > max_elapsed_time:
        if total_elapsed_time > max_elapsed_time:
            if proc.poll() is None:
                proc.terminate()
            time.sleep(polling_delay)
            break

        # otherwise, just wait

    # get the tail of the output file, after the result_prefix
    slines,errmsg = readfile(outfile_result)
    start_line = len(slines)
    if errmsg != '':
        slines = [dargs['result_prefix'],\
                  'Error: output file %s not written by game program' % outfile_result,\
                  errmsg]
    else:
        for i in range(len(slines)):
            if dargs['result_prefix'] in slines[i]:
                pos = slines[i].find(dargs['result_prefix'])
                slines[i] = slines[i][pos:]
                start_line = i

    output_tail = '\n'.join(slines[start_line+1:])
#    time_report = 'CPU-Time: %.2f, Elapsed time: %.2f\n' % (total_cpu_time,total_elapsed_time)
    time_report = 'Elapsed time: %.2f\n' % total_elapsed_time


    # close the stdout and stderr files
    try:
        f_stdout.close()
    except:
        pass

    try:
        f_stderr.close()
    except:
        pass

    slines,errmsg = readfile(outfile_stderr)
    if errmsg == '':
        print (time_report+output_tail+'\n'.join(slines))
    else:
        print (time_report+output_tail+'\n'+errmsg)

    # remove ancient output files...
    removeOldFiles('output-',10)

    Log(time_report)


# --------------------------------- Getargs -----------------------
def GetArgs():
    if HasTestArgs:
        return TestArgs
    dargs={}
    # try command-line
    for arg in sys.argv[1:]:
        if '=' in arg:
            parts=arg.split('=')
            if len(parts) > 1:
                if len(parts) == 2:
                    dargs[parts[0]] = parts[1]

    if 'progfile' not in dargs:
        # Try cgi
        cgitb.enable()
        form = cgi.FieldStorage()
        for key in form:
            dargs[key] = form[key].value

    return dargs

# ----------------------------- readfile ---------------------------
def readfile(filename):
    try:
        f = open(filename,'r')
        s = f.read()
        f.close()
    except:
        return [],'No file: %s\n' % filename
    if '\r\n' in s:
        s = s.replace('\r\n','\n')
    if '\r' in s:
        s = s.replace('\r','\n')
    return s.split('\n'),''

# ----------------------------------- removeOldFiles -------------------------
def removeOldFiles(prefix,nsecs):
    current_time = time.time()
    files = os.listdir('.')
    for afile in files:
        #print('looking at: ',afile)
        if afile.startswith(prefix) and \
           (afile.endswith('.txt') \
            or afile.endswith('.stdout') \
            or afile.endswith('.stderr')):
            #print ('checking: ',afile)
            access_time = os.stat(afile).st_mtime
            if current_time - access_time > nsecs:
                try:
                    os.remove(afile)
                except:
                    pass

# -------------------------------ChangeDirToHere -------------------------
def ChangeDirToHere():
    arg0 = sys.argv[0]
    pos1 = arg0.rfind('/')
    pos2 = arg0.rfind('\\')
    pos = max(pos1,pos2)
    if pos < 0:
        return
    here = arg0[:pos]
    os.chdir(here)

# ------------------------------------ Log ---------------------------------
def Log(msg):
    if Logging:
        try:
            f = open(Logfile,'a')
        except:
            return
        f.write(time.asctime()+', '+msg)
        f.close()

main()

#! /usr/bin/python

import sys

InteractiveHelp='''Command-line usage:
end-of-line.py -h
for command-line arguments'''

choices='''Choose new line ending:
1. no action
2. change to LF
3. Change to CRLF
4. Change to CR

Choice: '''

CommandLineHelp='''Change end-of-line characters, converting files in place.
-h [ this usage ]
LF file1 {file2 ... }  [ converts files to UNIX-style line ending ]
CRLF file1 {file2 ...} [ converts files to Windows-style line ending ]
CR files {file2 ...}   [ converts files to old Mac-style line ending ]
-s file1 {file2 ...}   [ show line endings for file(s) ]
'''

Endings1=['LF','CRLF','CR']
Endings2=['\n','\r\n','\r']

def main():
    if len(sys.argv)>1:
        command_line()
        return
    print (InteractiveHelp+'\n\n')
    print ('Checks and corrects end-of-line UNIX/Windows/Mac issues\n')
    fn = input('Name of file: ')
    show_eol(fn)
    action=input(choices)
    if action=='1':
        print ('Nothing changed.')
        return
    if not action in '234':
        print ('Bad choice.')
        return
    if action=='2':
        result=change_to(fn,'\n')
    elif action=='3':
        result=change_to(fn,'\r\n')
    elif action=='4':
        result=change_to(fn,'\r')

    if result=='':
        print ('File converted.')
    else:
        print (result)

def show_eol(filename):
    try:
        f=open(filename,'rb')
        sline=f.readline()
        f.close()
        ending=''
        if sline[-2:]=='\r\n':
            ending='CRLF'
        elif sline[-1]=='\n':
            ending='LF'
        elif sline[-1]=='\r':
            ending='CR'
        else:
            ending='unknown'
        print (filename+' ending is '+ending)

    except:
        print ('Error: cannot open '+filename)

def command_line():
    if sys.argv[1]=='-h':
        print (CommandLineHelp)
    elif sys.argv[1]=='-s':
        for i in range(2,len(sys.argv)):
            show_eol(sys.argv[i])
    elif sys.argv[1].upper() in Endings1:
        pos=Endings1.index(sys.argv[1].upper())
        new_ending=Endings2[pos]
        for i in range(2,len(sys.argv)):
            result=change_to(sys.argv[i],new_ending)
            if result=='':
                print ('Converted '+sys.argv[i])
            else:
                print (result)
    else:
        print ('Unknown arguments')

def change_to(filename,ending):
    f=open(filename,'rb')
    slines=f.readlines()
    f.close()
    f=open(filename,'wb')
    for sline in slines:
        f.write(sline.rstrip()+ending.encode())
    f.close()
    return ''

main()




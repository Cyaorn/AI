#! /usr/bin/env python3

# For PythonWebServer only!
# Game Startup: allows user to choose a file in cgi-bin as his competitor
#   Launches appropriate game UI with driver and competitor settings filled

# Usage: http://localhost:9000/cgi-bin/game-start.py?game={game-name}&competitor={competitor-filename}
#   game-name is one of: 'TicTacToe','Othello','Connect-4'

import os, sys, cgi, cgitb
cgitb.enable()

UIs = ['cgi-bin/TTT-webpage.html','cgi-bin/othello-ui.html','cgi-bin/connect-4-board.html']
Drivers = ['TimeDriver-py3.py','GameDriver-py3.py','GameDriver-py3.py']
IgnorePrograms = ['game-start.py'] + Drivers

HTML_Header = 'Content-type: text/html\n\n'

# --------------------------- main -------------------------
def main():
    form = cgi.FieldStorage()

    if 'game' not in form:
        showForm()
        return

    # Launch the game
    game = form['game'].value
    competitor = form['competitor'].value

    # Get the IP address/port
    ip = form['ip'].value.strip()
    if ip == '':
        showError('No IP address/port given')
        return

    # Choose driver
    if game == 'TicTacToe':
        ui = UIs[0]
        driver = Drivers[0]
    elif game == 'Othello':
        ui = UIs[1]
        driver = Drivers[1]
    elif game == 'Connect-4':
        ui = UIs[2]
        driver = Drivers[2]

    # make sure the driver is available
    driver = 'cgi-bin/'+driver
    try:
        f = open(driver,'r')
        f.close()
    except:
        showError('Driver file not found in cgi-bin: '+driver)
        return
    # Get UI file
    try:
        f = open(ui,'r')
        html = f.read()
        f.close()
    except:
        showError('Cannot open file: '+ui)
        return

    if ip[-1] != '/':
        ip += '/'
    html = html.replace('<!--<gamedriver>-->',ip+driver)
    if game == 'TicTacToe':
        competitor = 'cgi-bin/'+competitor
    html = html.replace('<!--<progfile>-->',competitor)

    # Launch
    print (HTML_Header+html)
    return

#--------------------------- showForm -------------------------
def showForm():
    files = [[filename.lower(),filename] for filename in os.listdir('cgi-bin') \
             if filename not in IgnorePrograms and filename.endswith('.py')]
    files.sort()

    f = open('cgi-bin/game-startup.html','r')
    html = f.read()
    f.close()
    comps = ''
    if len(files) == 0:
        comps = 'No competitor-like files inside cgi-bin'
    else:
        for afile in files:
            fname=afile[1]
            comps += '<a href="javascript:doit(\''+fname+'\');">'+fname+'</a><br/>\n'
    html = html.replace('<!--<competitors>-->',comps)
    print (HTML_Header+html)
    return

# ------------------------------ showError ------------------------------
def showError(errmsg):
    html = html_error.replace('<!--<errmsg>-->',errmsg)
    print (HTML_Header+html)
    return


html_error = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta content="en-us" http-equiv="Content-Language" />
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>Untitled 2</title>
</head>
<body>
<table border="1" align="center">
	<tr>
		<td><strong>&nbsp;<!--<errmsg>--><br />
		Press the Back button ...</strong>
		</td>
	</tr>
</table>
</body>
</html>
'''

main()


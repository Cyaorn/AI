#! /usr/bin/python3

# P. Brooks - Stuyvesant High School, Dec. 2018

# Startup driver for games
# Used by user to plant the correct URL's into the game front-end webpages
# Usage: http://..../startup.py
#    or
# Usage: http://..../startup.py?gamedriver={game driver program}&progfile={actual game program}
#  e.g.
# http://localhost:9000/startup.py?webpage=TTT-webpage.html&gamedriver=TimeDriver.py&progfile=TTT-Random.py

import cgi, cgitb
cgitb.enable()
import os


WebpageDefault = 'TTT-webpage.html'
GamedriverDefault = 'TimeDriver-py3.py'
GamedriverLoc = 'http://localhost:%s/cgi-bin/'

def main():
    form = cgi.FieldStorage()
    # Do we have all the info?
    progfile = GetFormValue(form,'progfile')
    webpage = GetFormValue(form,'webpage')
    if webpage == '': webpage = WebpageDefault
    gamedriver = GetFormValue(form,'gamedriver')
    if gamedriver == '': gamedriver = GamedriverDefault

    if progfile == '':
        print (HTML_Header+StartupHtml)
        return

    errmsg = FilesExist([webpage,gamedriver,progfile])
    if errmsg != '':
        ErrorOut(errmsg)
        return

    f = open('cgi-bin/'+webpage,'r')
    html = f.read()
    f.close()
    html = html.replace('<!--<progfile>-->','cgi-bin/'+progfile)
    port = os.environ['SERVER_PORT']
    game_filename = (GamedriverLoc % port) + gamedriver
    html = html.replace('<!--<gamedriver>-->',game_filename)
    print (HTML_Header+html)
    return

def GetFormValue(form,sname):
    if sname in form:
        return form[sname].value
    return ''

def FilesExist(lst):
    for filename in lst:
        try:
            f=open('cgi-bin/'+filename,'r')
            f.close()
        except:
            return '''Filename: "%s" doesn't exist in this directory''' % filename
    return ''

def ErrorOut(errmsg):
    s = ErrorPage.replace('<!--<errmsg>-->',errmsg)
    print (HTML_Header + s)
    return


HTML_Header = 'Content-type: text/html\n\n'
ErrorPage='''<html>
<body>
<table align="center" border="1">
<b>Error: <!--<errmsg>--></b>
</table>
</body>
</html>
'''

StartupHtml='''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta content="en-us" http-equiv="Content-Language" />
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>TicTacToe Startup</title>
<style type="text/css">
.auto-style1 {
	text-align: center;
}
.auto-style2 {
	border-style: solid;
	border-width: 1px;
	background-color: #CCFFFF;
}
</style>
</head>

<body>
<form method="get" action="startup.py">
<table align="center" class="auto-style2" border="1">
	<tr>
		<td class="auto-style1">TicTacToe Startup</td>
	</tr>
	<tr>
		<td>TicTacToe Python competitor filename:
		<input name="progfile" size="30" type="text" /></td>
	</tr>
	<tr>
		<td class="auto-style1">
		<input name="letsgo" type="submit" value="Let's go!" />&nbsp;</td>
	</tr>
	</table>
</form>

</body>

</html>
'''

main()





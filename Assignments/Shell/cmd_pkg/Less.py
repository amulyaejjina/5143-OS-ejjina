from multiprocessing.context import SpawnContext
import os,json,pydoc,sys
import pyautogui
from typing import KeysView
'''
--------------------------------------------------------------
LESS : Used to display page wise content of a file
Usage: less filename
       Up arrow/Down arrow to navigate
--------------------------------------------------------------
'''
from numpy import empty
with open(os.getcwd()+'/'+'Resources.json','r') as d:   # load keys from json module
    strings = json.load(d)                              # store it in a variable for further use   
from cmd_pkg import Getch 
getch = Getch.Getch() 
def less(**kwargs):
    command = ["less"]
    if 'params' in kwargs:
        params = kwargs['params']
    (term_width, term_height) = os.get_terminal_size() # get current terminal width,height
    if params:
        if os.path.exists(params[0]):
            fread = open(os.getcwd()+'/'+params[0],'r')
            content = fread.readlines()                # store lines in an array
            c = content[0:term_height]                 # get no of lines which are = terminal heigth
            c_str = ''.join(c)
            print(c_str)
        else:
            return ("Less: " +params[0]+ " "+strings['nof'])
        arrowCount = term_height

        while(True):                            # while loop to get arrow keys/Q
            char = getch()                      # waste a character
            if char in '\x1b':  
                a = getch()                     # waste a character
                direction = getch()  
                if direction in 'A':            # up arrow pressed
                    arrowCount = arrowCount - 1
                    width,height = pyautogui.position() # get current cursor position
                    pyautogui.move(0,height)    # move the cursor to desired height 
                    print(content[arrowCount])
                if direction in 'B' and arrowCount<(len(content)-1):      # down arrow pressed
                    if len(content)> term_height:
                        arrowCount = arrowCount + 1
                        print(content[arrowCount])  # get & keep printing one lineat the end of the terminal
            if char=='q':                       # if q,exit
                break
    else:
        return (strings['less'])                # if wrong formag,display message
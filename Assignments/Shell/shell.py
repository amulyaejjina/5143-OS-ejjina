#!/usr/bin/env python3
import os,re
'''
---------------------------------------------------------------------------------------
SHELL - The Driver program for the project
Desciprion - 1) Uses getch to get input as its being typed,     
             2) Parses the command entered
             3) Makes a call to Command_helper.py with parsed command,gets result back
             4) Prins it back to the terminal
             5) Waits for input again,repeats above steps until Ctrl+C/exit is keyed-in
NOTE : This program creates a 'history.txt' file to track history
       Please remove it from your home after you close the program.
---------------------------------------------------------------------------------------
'''
from binascii import b2a_hex
import json,sys
from numpy import empty
import command_helper
from cmd_pkg import *
from termcolor import colored
from pathlib import Path
from cmd_pkg import Grep
with open(os.getcwd()+'/'+'Resources.json','r') as d:
    strings = json.load(d)

getch = Getch.Getch()            # create instance of our getch class
prompt = "% "                    # set default prompt
pipeOutput = " "                 # Using a variable to differentiate btw calls(either its coming from piping or not)

def print_cmd(cmd):
    padding = " " * 80
    sys.stdout.write("\r"+padding)
    sys.stdout.write("\r"+os.getcwd()+prompt+cmd)
    sys.stdout.flush()

# Reference for below method pprint_list: Stackoverflow
def pprint_list(input_list):                            # This method is used to format the output of ls command
    (term_width, term_height) = os.get_terminal_size()  # Get terminal height and width
    if len((input_list))==0:     
        print("\n  No files present...")
        return
    elif len( str(input_list) ) <= term_width:          # if length of list is less than term width,just print with spaces
        print('\n'+'    '.join(input_list))
        return
    repr_list = [repr(x) for x in input_list]
    for i, x in enumerate(repr_list):
        x= x.replace("'", "")                           # replace ' with spaces for each list item
        if os.path.isdir(x):
            x = re.sub(x,colored(x,'cyan'),x)

    min_chars_between = 3                               
    min_element_width = min( len(x) for x in repr_list ) + min_chars_between # get min and max element widths
    max_element_width = max( len(x) for x in repr_list ) + min_chars_between
    if max_element_width >= term_width:                 # if the name of max element is more than terminal width,use only 1 column
        ncol = 1
        col_widths = [1]
    else:
        # Start with max possible number of columns and reduce until it fits
        ncol = min( len(repr_list), term_width // min_element_width  )
        while True:
            col_widths = [ max( len(x) + min_chars_between \
                                for j, x in enumerate( repr_list ) if j % ncol == i ) \
                                for i in range(ncol) ]
            if sum( col_widths ) <= term_width: break
            else: ncol -= 1

    sys.stdout.write('\n')
    for i, x in enumerate(repr_list):
        x= x.replace("'", "")
        sys.stdout.write( x.ljust( col_widths[ i % ncol ] ) )
        if i == len(repr_list) - 1:
            sys.stdout.write('\n')
        elif (i+1) % ncol == 0:
            sys.stdout.write('\n')

def get_rediret_char(cmd): # Method to get type of redirection(append/write) in given command
    redirect_char=''
    if '>>' in cmd:
        redirect_char = '>>'
    elif '>' in cmd:
        redirect_char = '>'
    return redirect_char

#----------------- STARTING: Recursive method to execute piping  ------------------------

def process_piping(input,pre_output): 
    global pipeOutput
    if(len(input)):          # in input,we'll get list of commands i.e. ['grep b a.py','wc -l']
        a = input[0].split() # takes each item of list which is each command i.e. ['grep', 'b','a.py']
        cmd = a[0]           # gets command i.e. 'grep'
        params = a[1:]       # gets params i.e.  ['b','a.py']
        if ch.exists(cmd):   # check if its a valid command
            pipeOutput = ch.invoke(cmd=cmd, params=params,thread=False,ispiping=pre_output) # invokes command
        else:
            pipeOutput = "Error: command %s doesn't exist." % (cmd) #catches exceptions
        input.pop(0)         # remove commands(list items) from list after they are executed
        return process_piping(input,pipeOutput) # pass output from line 91 to next recursive call and so on till end of list
    else:
        return pipeOutput    # returns the last output of the pipe

if __name__ == '__main__':
    arrowCount = 1
    ch = command_helper.CommandHelper()
    b = command_helper.bcolors()
    cmd=''
    print_cmd(cmd) 
    getch = Getch.Getch()

#----------------------- STARTING: Getch loop to constantly read chars from terminal---------------------
    while True:
        char = getch()
        home = Path.home()
        if char == '\x03' or cmd == 'exit': # ctrl-c / exit is given
            raise SystemExit("Bye.")
        elif char == '\x7f':                # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)
        elif char in '\x1b':                            # Any of the arrow key is pressed
            a = getch()                                 # waste a character
            direction = getch()                         # grab the direction
            if direction in 'A':                        # if up arrow is pressed
                arrowCount = arrowCount + 1             # Counting the no of times up arrow is pressed
                with open(os.path.join(home,'history.txt')) as f: # get history file
                    last_cmd = f.read()
                    last_cmd=last_cmd.split('\n')       # store each line as a item in a list
                    if arrowCount<len(last_cmd):        # catch exception when count of arrow presses are greater than content length
                        sys.stdout.flush()
                        padding = " " * 80
                        sys.stdout.write("\r"+padding)
                        sys.stdout.write("\r"+os.getcwd()+prompt+last_cmd[len(last_cmd)-arrowCount]) # subtracting no of arrow click from history file from bottom to display it
                        cmd = last_cmd[len(last_cmd)-arrowCount] # this is to put the displayed command in cmd,as its not building by getch
            if direction in 'B' and arrowCount>1:       # down arrow pressed
                arrowCount = arrowCount - 1             # keeping track of arrow count
                with open(os.path.join(home,'history.txt')) as f:
                    last_cmd = f.read()
                    last_cmd=last_cmd.split('\n')       # store each line as a item in a list
                    sys.stdout.flush()
                    padding = " " * 80
                    sys.stdout.write("\r"+padding)
                    sys.stdout.write("\r"+os.getcwd()+prompt+last_cmd[len(last_cmd)-arrowCount]) # based on arrow click fetch the line from file and display it
                    cmd = last_cmd[len(last_cmd)-arrowCount] # this is to put the displayed command in cmd,as its not building by getch
            if direction in 'C':                        # Doing nothing
                pass
                #print("right arrow")
            if direction in 'D':                        # Doing nothing 
                pass          
                #print("left arrow")
  
        elif char in '\r':                              # Enter is pressed
            command='' 
#----------------------------- STARTING: Command parsing---------------------------------------

            if(cmd.strip()):   # This IF block is for parsing commands based on the input charachters
                home = Path.home()
                if not cmd.startswith('!'):             # Dont store commands starting with ! in history
                    if not os.path.exists(os.path.join(home,'history.txt')): # create history.txt for the first time in users home
                        f = open(os.path.join(home,'history.txt'),'w')
                        f.close()
                    history_data = open(os.path.join(home,'history.txt'),'a')
                    history_data.write(cmd+'\n')        # Write commands to histiory file as enter is clicked
                    history_data.close()
                type_of_redirect=get_rediret_char(cmd)
                if (('>' or '>>') in cmd) and (('|') in cmd): # If the command has both | and >/>>,split on >/>>
                    left,right = cmd.split(type_of_redirect)
                    commands_list = left.split('|') # put series of commands in a list to pass to recursive method
                    c = commands_list[0].split()
                    command = c[0]
                elif ('>' or '>>') in cmd:              
                    left,right=cmd.split(type_of_redirect) # If the command has >/>>,split on >/>>,save right part
                    left = left.split()
                    command=left[0]                        # get command key word
                    params=left[1:len(left)]               # get params
                elif '|' in cmd:                           # If the command has |,split on |
                    commands_list = cmd.split('|')
                    c = commands_list[0].split()           # get first command key word
                    command = c[0]
                elif '|' not in cmd and not type_of_redirect: # if its a simple command
                    cmd_split = cmd.split()
                    command = cmd_split[0] 
                    params = cmd_split[1:] 
            if command.startswith('!') and command[1:].isdigit():# If !,change the command to a given name for execution
                    params = command
                    command = 'historybynum'  
            if command == 'man':        # If man is given,fetch that key from json file and print
                mydocstring = strings[params[0]+"_man"]
                print('\n'+mydocstring)  

#-------------------- STARTING : INVOKING SPECIFIC METHODS BASED ON PARSED COMMAND ------------------

            if (command != 'man') and (ch.exists(command)): #This if block is to execute command and print results
                if '|' in cmd:
                    if 'ls' in cmd:
                        a = process_piping(commands_list,'frompiping') # call recursive method,if its from piping,let the method know
                    else:
                        a = process_piping(commands_list,'') # call recursive method for processing
                    if ('>' or '>>') not in cmd:
                        print('\n')
                        print(a)
                else:
                    a = ch.invoke(cmd=command, params=params,thread=False,ispiping="")# call invoke if not piping

#-------------------- STARTING : Displaying result to terminal --------------------------------------

                if '>>' in cmd:        # append to file if >> is present
                    f = open(right.strip(),'a')
                    f.write(a)
                    f.close()
                    print('\r')
                elif '>' in cmd:       # write to file if > is present
                    f = open(right.strip(),'w')
                    f.write(a)
                    f.close()
                    print('\r')
                elif(a is None):       # If nothing is returned,dont print anything, ex: for mv/cp we'll not have o/p
                    print('\r')
                elif '|' not in cmd and a is not None:
                    if command == 'ls':
                        pprint_list(a) # if ls,call formatting method to display in a orderly manner
                    elif command == 'wc':
                        print('\n'+'\t'+a)
                    elif command == 'historybynum':
                        a=a.strip('\n')
                        sys.stdout.write('\n'+os.getcwd()+prompt+a) # if !x is given,just print out the fetched command from history
                        cmd = a
                    else:
                        if type(a) is str:
                            print('\n'+a)  # print result to terminal
                        else:
                            print(a)
                if command == 'historybynum':
                    cmd=a              # If its !(num),display that fetched command from history to terminal
                else:
                    cmd=''
                    print_cmd(cmd)
            else:
                if(command != 'man') and (len(command)>0): # check for any gibberish given and handle
                    print("\n"+ "Error: command %s doesn't exist." % (command))
                    cmd=''
                    print_cmd(cmd)
                else:
                    sys.stdout.write('\n')
                    cmd=''
                    print_cmd(cmd)

        else:
            cmd += char                 # keep building command to variable 'cmd' if only characters are being entered
            print_cmd(cmd) 

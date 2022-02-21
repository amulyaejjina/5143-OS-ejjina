'''
--------------------------------------------------------------
GREP : Used as a filter to get output based on a word hit/match
Usage: grep searchpattern filename
       grep -l searchpattern filename
Used REGEX to color target word
--------------------------------------------------------------
'''
import os,json,re
from termcolor import colored
with open(os.getcwd()+'/'+'Resources.json','r') as d:    # load strings from json module 
    strings = json.load(d)                               # store it in a variable for further use

def grep(**kwargs):
    command = ["grep"]
    a=''                                                 # a common variable to return content
    if 'params' in kwargs:
        params = kwargs['params']
    if kwargs['ispiping']:                               # if the method call is comimg from PIPING
        output = kwargs['ispiping']
        output = output.split('\n')
        params = kwargs['params']
        if(len(params)==2 and params[0]=='-l'):          # this is for format :"grep -l text"
           for line in output:  
                if params[1] in line:
                    return 'standard input'
        elif(len(params)==1):                            # this is for format : "grep text"
            for line in output:  
                if params[0] in line:
                    a=a+line+'\n'
                    # Using REGEX to substitute target word with colored word
                    a = re.sub(params[0],colored(params[0],'red'),a) 
            return a
        else:
            return strings['format']                     # if wrong format is given,display message
        return a 
    else:                                                # if method call is not from Piping
        # this is for format :"grep -l text a.py"
        if len(params)>2:                                
            if params[0] == '-l':
                if os.path.isfile(params[2]):
                    fread = open(os.getcwd()+'/'+params[2],'r')
                    content = fread.readlines()
                    for line in content:  
                        if params[1] in line:
                            return params[2]
                else:
                    return strings['nof']+params[1]
        # this is for format : "grep text a.py"
        elif len(params)>1:                              
            if os.path.isfile(params[1]):                # checking given file existence
                fread = open(os.getcwd()+'/'+params[1],'r')
                content = fread.readlines()
                for line in content:  
                    if params[0] in line:
                        a=a+line
                        # Using REGEX to substitute target word with colored word
                        a = re.sub(params[0],colored(params[0],'red'),a)
                return a
            else:
                return strings['nof']+params[1]          # display file not exist message
        else:                                            # if wrong format is given,display message    
            return (strings['grep'])
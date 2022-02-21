import os,json,shutil
'''
--------------------------------------------------------------
HISTORYBYNUM : This is used to fetch the command from history          
Usage: ! (number of command from history)
--------------------------------------------------------------
'''
from pathlib import Path
with open(os.getcwd()+'/'+'Resources.json','r') as d:    # load keys from json module
    strings = json.load(d)                               # store it in a variable for further use 
def historybynum(**kwargs):
    command = ["historybynum"]
    content=''
    params = kwargs['params']
    home = Path.home()                                   # get user home
    if os.path.exists(os.path.join(home,'history.txt')): # check if file exists,then read
        fread = open(os.path.join(home,'history.txt'),'r')
        a=fread.readlines()
        num = int(params[1:])                            # ex: "!2" - so ignore ! & get [1:]
        if num < len(a) and num>0:                       
            return a[num]                                # as we have a list,access the element and return
    return content
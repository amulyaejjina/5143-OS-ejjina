import os,json,shutil
'''
--------------------------------------------------------------
HISTORY : This is used to print all the history of commands
          entered on the terminal
Usage: history
--------------------------------------------------------------
'''
from pathlib import Path
with open(os.getcwd()+'/'+'Resources.json','r') as d:   # load keys from json module
    strings = json.load(d)                              # store it in a variable for further use    
def history(**kwargs):
    command = ["history"]
    content=''
    params = kwargs['params']
    home = Path.home()                                  # get user home
    if os.path.exists(os.path.join(home,'history.txt')):# check if file exists,then read it
        fread = open(os.path.join(home,'history.txt'),'r')
        a=fread.readlines()
        i=1
        for i in range(1,len(a)):                       # append line nos & print whole file to terminal 
            content = content+str(i)+' '+a[i]
        return content
    return content
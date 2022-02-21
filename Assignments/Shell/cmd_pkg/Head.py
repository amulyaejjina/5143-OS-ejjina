import os,json
'''
--------------------------------------------------------------
HEAD : Used to get first 10/given number of lines from files
Usage: head filename (default 10 lines)
       head -n 10 filename
       head -10 filename
--------------------------------------------------------------
'''
from itertools import islice
with open(os.getcwd()+'/'+'Resources.json','r') as d:  # load strings from json module 
    strings = json.load(d)                             # store it in a variable for further use
def head(**kwargs):
    command = ["head"]
    content=""
    if kwargs['ispiping']:                             # if the method call is comimg from PIPING..(cont)
        output = kwargs['ispiping']                    #.. remove all file operations,use prev output
        output = output.split('\n')
        params = kwargs['params']
        x = 0
        # for format - "head -n 10 a.py"
        if(len(params)==2 and params[0]=='-n' and params[1].isdigit()):
            x = int(params[1])
            for i in output[:x]:
                content = content+i
        # for format - "head -10 a.py"
        elif(len(params)==1 and params[0].startswith("-") and params[0][1:].isdigit()):
            x = int(params[0][1:])
            for i in output[:x]:
                content = content+i+'\n'
        # for format - "head a.py"
        elif(len(params)==0):
            x = 10
            for i in output[:x]:
                 content = content+i+'\n'
        else:
            return strings['format']
        return content 
    else:
        if 'params' in kwargs:
            params = kwargs['params']
        if len(params)>1:
            linesneeded=0
            # for format - "head -10 a.py"
            if(len(params)==2):
                file_name=params[1]
                if params[0].startswith("-") and params[0][1:].isdigit():
                    linesneeded = abs(int(params[0]))
                else:
                    return strings['format']
            # for format - "head -n 10 a.py"
            elif(len(params)==3):
                file_name=params[2]
                if isinstance(int(params[1]),int):
                    linesneeded = abs(int(params[1]))
            if os.path.isfile(file_name):
                if linesneeded != 0 and isinstance(linesneeded,int):
                    with open(file_name) as f:
                        for line in islice(f, linesneeded):
                            content=content+line
                else:
                    return(strings['notint'])
            else:
                return (" head: "+ file_name +": "+strings['nof'])
        # for format - "head a.py"
        elif len(params)==1:
            if os.path.isfile(params[0]):
                with open(params[0]) as f:
                    for line in islice(f, 10):
                        content=content+line
            else:
                return (" head: "+ params[0] +": "+strings['nof'])
        else:
            return strings['format']
    return content
import os,json
'''
--------------------------------------------------------------
TAIL : Used to get first 10/given number of lines from files
USAGE: tail filename (default 10 lines)
       tail -n 10 filename
       tail -10 filename
--------------------------------------------------------------
'''
from itertools import islice
# load keys from json module for strings
with open(os.getcwd()+'/'+'Resources.json','r') as d:
    strings = json.load(d)

def tail(**kwargs):
    command = ["tail"]
    content=""
    # if method call is from piping - 
    if kwargs['ispiping']:
        output = kwargs['ispiping']
        output = output.split('\n')
        params = kwargs['params']
        x = 0
        # for format : tail -n 10, slice the last lines from content list
        if(len(params)==2 and params[0]=='-n' and params[1].isdigit()):
            x = int(params[1])
            for i in islice(output,len(output)-x,len(output)):
                content=content+i+'\n'
        # for format : tail -10, slice the last lines from content list
        elif(len(params)==1 and params[0].startswith("-") and params[0][1:].isdigit()):
            x = int(params[0][1:])
            for i in islice(output,len(output)-x,len(output)):
                content=content+i+'\n'
        # for format : tail, slice the last 10 from content list
        elif(len(params)==0):
            for i in islice(output,len(output)-10,len(output)):
                content=content+i+'\n'
        else:
            return strings['tail_m']
        return content
    # if method call is not from piping - 
    else:
        if 'params' in kwargs:
            params = kwargs['params']
        if len(params)>1: 
            # Get the no of lines to display in a variable based on format
            # for format : tail -n 10, slice the last lines from content list 
            if(len(params)==3 and params[0]=='-n' and params[1].isdigit()):
                file_name=params[2]
                linesneeded = int(params[1])
            # for format : tail -10, slice the last lines from content list
            elif(len(params)==2 and params[0].startswith("-") and params[0][1:].isdigit()):
                file_name=params[1]
                linesneeded = int(params[0][1:])
            else:
                return strings['tail_m']
            # check whether given filename exists
            if os.path.isfile(file_name):
                if linesneeded != 0 and isinstance(linesneeded,int):
                    with open(file_name) as f:
                        lcount = len(f.readlines())
                        # if given line number os greater than content length,show complete file content
                        if linesneeded>lcount:
                            with open(file_name) as f:
                                a = f.readlines()
                                content = ''.join(a)
                        else:
                            # slice the needed no of lines from last of the content list
                            with open(file_name) as f:
                                for line in islice(f,lcount-linesneeded,lcount):
                                    content=content+line
                else:
                    return(strings['notint'])
            else:
                # display specific error message
                return (" tail: "+ file_name +": "+strings['nof'])
        elif len(params)==1:
            # for format : tail filename (default 10 lines)
            if os.path.isfile(params[0]):
                with open(params[0]) as f:
                    lcount = len(f.readlines())
                    # if len of content is <10,display whole content
                    if lcount<=10:
                        with open(params[0]) as f:
                            a = f.readlines()
                            content = ''.join(a)
                    else:
                        # slice last 10 lines and return
                        with open(params[0]) as f:
                            for line in islice(f, lcount-10,lcount):
                                content=content+line
            else:
                return (" tail: "+ params[0] +": "+strings['nof'])
        else:
            return(strings['format'])
        return content
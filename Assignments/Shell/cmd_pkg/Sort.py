import os,json
'''--------------------------------------------------------------
SORT : Used to sort given file
Usage: sort filename 
--------------------------------------------------------------'''
with open(os.getcwd()+'/'+'Resources.json','r') as d:  # load keys from json module
    strings = json.load(d)                             # store it in a variable for further use

def sort(**kwargs):
    command = ["sort"]
    content=''
    if 'params' in kwargs:
        params = kwargs['params']            # get params from kwargs
    if kwargs['ispiping']:                   # if the method call is comimg from PIPING,use passed ouput
        output = kwargs['ispiping']          # read passed output from prev command
        output = output.split('\n') 
        if not params:
            output.sort()                    # sort the output passed
            l = '\n'.join(output)
            content = content+l
            return content                  
    else:                                    # if not from PIPING
        if params:
            if os.path.isfile(params[0]):    # check whether file exists
                with open(params[0]) as f:
                    a = f.readlines()        # read the contents of file
                    a.sort()
                    b = ''.join(a)
                    return b                 # sort and return the sorted content
            else:
                return strings['nof']+params[0]
        else:
            return (strings['chmod'])        # if wrong format,display message

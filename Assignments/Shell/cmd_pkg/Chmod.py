import os,json
'''
--------------------------------------------------------------
CHMOD : Modifies permissions of file
Usage: chmod 777 filename
--------------------------------------------------------------
'''
with open(os.getcwd()+'/'+'Resources.json','r') as d:   # load strings from json module
    strings = json.load(d)                              # store it in a variable for further use

def chmod(**kwargs):
    command = ["chmod"]
    if 'params' in kwargs:
        params = kwargs['params']                        # loading params from kwargs
    if params and len(params)>1 and params[0].isdigit(): # checking the length of the params & if it is a digit or not
        for item in params[0]:                           # for loop iterating the digits i.e 777
            if int(item)>7:                              # restrict if >7 is given
                return strings['chmod_check']            # return a string from json for error handling
        if os.path.isfile(params[1]):                    # checking is given test is a file or not
            os.chmod(params[1],int(params[0],8))         # using os module to alter permissions
        else:
            return strings['nof']+params[1]              # return a string from json for error handling
    else:
        return (strings['chmod'])                        # return a string from json for error handling

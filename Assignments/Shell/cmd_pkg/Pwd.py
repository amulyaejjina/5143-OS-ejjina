import os,json
'''
--------------------------------------------------------------
PWD : Displays current working directory
USAGE:  pwd
        pwd -L : current working directory,similar to pwd
        pwd -p : gets actual path if its a link
--------------------------------------------------------------
'''
with open(os.getcwd()+'/'+'Resources.json','r') as d:       # load keys from json module
    strings = json.load(d)                                  # store it in a variable for further use
def pwd(**kwargs):
    command = ["pwd"]
    if 'params' in kwargs:
        params = kwargs['params']                           # get params from kwargs 
    if (params and params[0]=='-L') or (not params):        # for format : "pwd -L" or "pwd"
        return os.getcwd()
    elif params and params[0]=='-P':                        # for format : "pwd -L"
        return (os.readlink(os.getcwd()))
    elif len(params)>=1 and params[0]:                      # if wrong format,display message
        return strings['pwd']

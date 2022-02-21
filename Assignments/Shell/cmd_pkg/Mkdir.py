import os,json
'''
--------------------------------------------------------------
MKDIR : Used to make directories
Usage: mkdir dirname      : Create a single directory
       mkdir -p dir1/dir2 : Create intermediate directories as required.
       mkdir dir1 dir2    : Create multiple directories at once
--------------------------------------------------------------
'''
with open(os.getcwd()+'/'+'Resources.json','r') as d:     # load keys from json module
    strings = json.load(d)                                # store it in a variable for further use
def mkdir(**kwargs):
    command = ["mkdir"]
    if 'params' in kwargs:
        params = kwargs['params']                         # get params from kwargs
    else:
        params = []
    if params:
        if len(params)>1 and params[0]=='-p':             # for format : "mkdir -p dir1/dir2/dir3"
            path = os.path.join(os.getcwd(), params[1])
            os.makedirs(path)
        elif len(params)>1 :                              # for format : "mkdir dir1 dir2 dir3"
            for item in params:
                path = os.path.join(os.getcwd(), item)
                os.mkdir(path)
        elif len(params)==1 and params[0]=='-p':          # wrong format : display message
            return (strings['mkdir'])
        elif params[0]:                                   # for format : "mkdir dir1"
            cmd = params[0]
            path = os.path.join(os.getcwd(), cmd)
            try: 
                os.mkdir(path)
            except:
                return "Directory already exists..."      # if directiry already exists
        else:
            return (strings['mkdir'])
    else:
        return (strings['mkdir'])                        # if wrong format,display message
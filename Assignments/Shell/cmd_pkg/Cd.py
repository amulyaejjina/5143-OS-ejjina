import os,json
'''
--------------------------------------------------------------
CD : Changes Directory
Usage: Cd
       Cd ~
       Cd ..
       Cd .. ..
       Cd directory/path
--------------------------------------------------------------
'''
with open(os.getcwd()+'/'+'Resources.json','r') as d:             # load strings from json module
    strings = json.load(d)                                        # store it in a variable for further use
def cd(**kwargs):
    command = ["cd"]
    if 'params' in kwargs: 
        params = kwargs['params']                                 # loading params from kwargs
    current_dir = os.getcwd()                                     # get current directory
    if params and params[0]=="..":                                # This if for going to parent directory(1-level up)                               
        a = current_dir.split('/')                                
        if len(params)>1 and params[0]==".." and params[1]=="..": # if .. .. is given go back up to two parent directories
            a=a[:len(a)-2]                                        # backimg up 2 levels                                      
        else:
            a=a[:len(a)-1]                                        # backimg up 1 level
        if current_dir == '/Users':                               # If it is Users,show only root(/) from next even though cd .. is given
            b='/'
        else:
            b='/'.join(a)
        try:
            os.chdir(b)                                           # change directory and catch execption if any
        except:
            return '\r'+strings['nof']+ b                         # Display string from json file if exception was encountered
    elif not params or params[0]=="~":                            # If cd/cd ~ - take to home directory
        a=os.environ['HOME']                                      # get home
        os.chdir(a)                                               # changing directory to home
    elif params[0]:                                               # if a path is given after cd,change to specific path
        p=current_dir+"/"+params[0]                               # add given path to current path
        try:
            os.chdir(p)                                           # change directory and catch execption if any
        except:
            return strings['nof']+ params[0]                      # Display string from json file if exception was encountered

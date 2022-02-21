import os,json
'''
--------------------------------------------------------------
CP : Copies content from one file to another
Usage: cp filename1 filename2
       cp directory1/filename1 directory2/filename2
       cp filename1 dir/filename1
--------------------------------------------------------------
'''
with open(os.getcwd()+'/'+'Resources.json','r') as d:        # load strings from json module               
    strings = json.load(d)                                   # store it in a variable for further use
def cp(**kwargs):
    path=os.getcwd()
    if 'params' in kwargs:
        params = kwargs['params']                            # loading params from kwargs
    if len(params)>1:
        conc=path+"/"+params[0]
        if os.path.exists(params[0]):                        # check if copy from file exists
            fread=open(params[0],'r')                        # read the file
            content=fread.read()                             # store the content fromr read
            if '/' in params[1]:                             # if a directory is given in COPY TO
                parm_split = params[1].split('/')            # split it on /
                pa2 = parm_split[0]                          # This variable is to check given directory exist or not
                if len(parm_split)==3:
                    pa = os.path.join(parm_split[0],parm_split[1],parm_split[2])       
                else:
                    pa = os.path.join(parm_split[0],parm_split[1])
            else:                                            # If only filename is given in COPY TO
                onlyfile = True
                pa = pa2 = params[1]
            if os.path.exists(pa2) or onlyfile:              # check given directory exist or not/if its a file
                fread2 = open(pa,'w')                        # open the file
                fread2.write(content)                        # read the file
            else:
                 return (" cp: "+ pa2 +": "+strings['nof'])  # display error string if target diretcory doesnt exist
        else:
            return (" cp: "+ params[0] +": "+strings['nof']) # display error if COPY FROM file doesnt exist
    else:
        return (strings['cp'])                               # display format of usage, if no paramters are given

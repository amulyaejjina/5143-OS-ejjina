import os,json,shutil
'''
--------------------------------------------------------------
MV : This is used to move files from one directory to another
USAGE: mv dir1/file1 dir2/file2
       mv file1 file2
       mv file dir
--------------------------------------------------------------
'''
with open(os.getcwd()+'/'+'Resources.json','r') as d:       # load keys from json module
    strings = json.load(d)                                  # store it in a variable for further use
def mv(**kwargs):
    command = ["mv"]
    params = kwargs['params']                               # get params from kwargs
    if len(params)>1:                                       # for formats given in usage above
        if os.path.exists(params[0]):
            shutil.move(os.getcwd()+"/"+params[0],os.getcwd()+"/"+params[1])# using shutil to move files
        else:
            return ("mv: rename " +params[0] +" "+strings['nof'])
    else:
        return (strings['mv'])                              # if wrong format,display message
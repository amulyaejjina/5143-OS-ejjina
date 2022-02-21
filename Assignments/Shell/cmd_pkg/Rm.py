import os,json,shutil
'''
--------------------------------------------------------------
RM : Removes a file/directory
Usage: rm Filename
       rm -rf dFrectory
       rm -d file
--------------------------------------------------------------
'''
# load keys from json module
with open(os.getcwd()+'/'+'Resources.json','r') as d:
    strings = json.load(d)

def rm(**kwargs):
    command = ["rm"]
    params = kwargs['params']
    if params:
        # get current path based on parameters
        if len(params)>1:
            currentpath1 = os.getcwd()+"/"+params[1]
        else:
            currentpath0 = os.getcwd()+"/"+params[0]
        if len(params)>1:
            # rm -rf directory
            if params[0]=='-rf' and os.path.isdir(currentpath1):
                shutil.rmtree(os.getcwd()+"/"+params[1])
            # rm -rf file
            if params[0]=='-rf' and os.path.isfile(currentpath1):
                os.remove(params[1])
            # rm -d file
            elif params[0]=='-d' and os.path.isfile(currentpath1):
                os.remove(params[1])
            # rm -d directory : Directory not empty
            elif params[0]=='-d' and os.path.isdir(currentpath1) and (len(os.listdir(currentpath1))!=0):
                return ("rm:"+params[1]+"h: Directory not empty")
            # rm -d directory : If Directory is empty,delete
            elif params[0]=='-d' and os.path.isdir(currentpath1) and (len(os.listdir(currentpath1))==0):
                os.rmdir(params[1])
        elif len(params)==1:
            # rm -d :  Display message saying give correct format
            if params[0]=='-d':
                return (strings['rm'])
            # rm Directiry : Display message saying its a directory
            elif os.path.isdir(currentpath0):
                return ("rm: "+ params[0]+" : is a directory")
            # rm File : Remove file
            elif os.path.isfile(currentpath0):
                os.remove(params[0])
            # rm File : No File present
            elif not os.path.isfile(currentpath0):
                return ("No such file"+params[0])
    else:
        return (strings['rm'])
import os,json
'''
--------------------------------------------------------------
CAT   : Displays content of a file/files on the terminal
Usage : Cat Filename/Filenames
--------------------------------------------------------------
'''
with open(os.getcwd()+'/'+'Resources.json','r') as d:       # load strings from json file
    strings = json.load(d)                                  # store it in a variable for further use
def cat(**kwargs):
    command = ["cat"]
    if 'params' in kwargs:                                  # loading params from kwargs
        params = kwargs['params']
    content=""                                              # empty string to store concatenated output
    error=""
    if kwargs['ispiping']:                                  # checking if the call is coming from piping
        output = kwargs['ispiping']   
        if not params:                                      # if not params,take piped output whichis passed as input here
            content = content+output                        # add it to the content
            return content                                  # return it to get it printed to terminal
    if len(params)>=1:                                      # if multiple files are given to cat
        for i in range(len(params)):                        # run a loop for all files
            if os.path.exists(params[i]):                   # check if the given file is present or not
                fread=open(params[i],'r')                   # open each file
                a = fread.read()                            # read each file
                content = content + a                       # add contents of each file to variable 'content'
                fread.close()               
            else:
                error = error+"cat: " +params[i]+": "+strings['nof']+"\n" # error handling in case of nof files found
        if len(error)>=1:                                   # if an error is caught,return it to get it printed
            return error
        else:
            return content                                  # if no error is found,retuen content
    else:
        return strings['format']                            # this means no parms are given,show format in terminal
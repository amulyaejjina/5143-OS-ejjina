import os,json,re
'''
--------------------------------------------------------------
WC : Used to get number of lines,words,chars
Usage: wc filename (by default gives all three l,w,c)
       wc -l : Gives just lines
       wc -w : Gives just words
       wc -c : Gives just chars
       wc -l -w : Gives lines + chars
--------------------------------------------------------------
'''
# load keys from json module for strings
with open(os.getcwd()+'/'+'Resources.json','r') as d:
    strings = json.load(d)

def wc(**kwargs):
    command = ["wc"]
    lines=0
    words=0
    chars=0
    value=''
    # if method call is from piping - 
    if kwargs['ispiping']:
        output = kwargs['ispiping']
        output_split = output.split('\n')
        params = kwargs['params']
        # get no of lines,words
        for line in output_split:
            lines = lines+1
            for word in line.split():
                words=words+1
        # Using REGEX to remove escape charachters & get no of chars
        ansi_escape = re.compile(r'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])')
        result = ansi_escape.sub('', output)
        chars = len(result)
        # format the output based on command
        # for format : wc -l
        if(len(params)==1 and params[0][0]=='-' and params[0][1:].isalpha()):
            if params[0]=='-l':
                value =value+str(lines)
            elif params[0]=='-w':
                value =value+str(words)
            elif params[0]=='-c':
                value =value+str(chars)
            else:
                return strings['wc_m']
        # for format : wc (show all l,w,c)
        elif(len(params)==0):
            value =value+'   '.join(map(str, (lines,words,chars)))
        # Handle exceptions
        else:
            return strings['wc_m']
        return value 
    else:
        if 'params' in kwargs:
            params = kwargs['params']
        length = len(params)
        if len(params)>=1:
            if len(params)==1:
                index=0
            elif len(params)>1:
                index = len(params)-1
            # check whether given file exists
            if os.path.exists(params[index]):
                path = os.getcwd()+'/'+params[index]
                # get no of lines,words,chars by iterating through read content
                for line in open(path,'r').readlines():
                    lines = lines+1
                    for word in line.split():
                        words = words+1
                chars = len(open(params[index]).read())
                # format the output based on command
                # for format : wc -l / wc -l -w
                if length>1:
                    for i in range(0,length-1):
                        if params[i]=='-l':
                            value =value+ '   '.join(map(str, (lines,params[index])))
                        elif params[i]=='-w':
                            value =value+ '   '.join(map(str, (words,params[index])))
                        elif params[i]=='-c':
                            value =value+ '   '.join(map(str, (chars,params[index])))
                # for format : wc (show all l,w,c)
                else:
                        value =value+ '   '.join(map(str, (lines,words,chars,params[0])))
                return value 
            else:
                # display error for FileNotFound exception
                return strings['nof']
        else:
            # display error message if wrong format
            return(strings['wc'])


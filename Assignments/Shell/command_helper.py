'''
---------------------------------------------------------------------------------------
COMMAND_HELPER - Acts as a middle layer & Ties in the shell.py and command_package
Desciprion - 1) This is used to call respective method in the form of 
                 accessing element of dictionary
             2) When invoke is being called by shell.py,this program inturn calls each 
                 command method from package
NOTE : This program creates a 'history.txt' file to track history
       Please remove it from your home after you close the program.
---------------------------------------------------------------------------------------
'''
from asyncore import write
from email import contentmanager
from pickletools import read_uint1
import pydoc
import sys
import os
import shutil
from itertools import islice
from pydoc import pager
import json
from zipapp import get_interpreter
from tabulate import tabulate
from cmd_pkg import *

class bcolors:               # ANSI escape codes for coloring of text
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CommandHelper(object):
    def __init__(self):
        pass
        # maintaining list of all available commands here for exists method
        self.commands = {}
        self.commands['ls'] = Ls.ls         
        self.commands['rm'] = Rm.rm
        self.commands['mv'] = Mv.mv
        self.commands['cp'] = Cp.cp
        self.commands['less'] = Less.less
        self.commands['cd'] = Cd.cd
        self.commands['cat'] = Cat.cat
        self.commands['pwd'] = Pwd.pwd
        self.commands['mkdir'] = Mkdir.mkdir
        self.commands['exit'] = Exit.exit
        self.commands['head'] = Head.head
        self.commands['tail'] = Tail.tail
        self.commands['grep'] = Grep.grep
        self.commands['wc'] = Wc.wc
        self.commands['chmod'] = Chmod.chmod
        self.commands['sort'] = Sort.sort
        self.commands["history"]=History.history
        self.commands["historybynum"]=Historybynum.historybynum
        self.commands["c"]=C.c

    def invoke(self, **kwargs):
        # unpack parameters from kwargs and put them in specific variables i.e.cmd,params,...etc
        cmd = kwargs.get("cmd", None)
        params = kwargs.get("params", None)
        flags = kwargs.get("flags", None)
        # using the below parameter to check whether call is made from piping
        ispiping = kwargs.get("ispiping",None)  
        
        # creating a dictionary to store command definitions
        # Adding Method names to dictionary as key values
        commands = {}                       
        commands["cd"] = Cd.cd              
        commands["ls"] = Ls.ls
        commands["head"] = Head.head
        commands["tail"] = Tail.tail
        commands["rm"] = Rm.rm
        commands["mv"] = Mv.mv
        commands['cp'] = Cp.cp
        commands['less'] = Less.less
        commands["cat"] = Cat.cat
        commands["pwd"] = Pwd.pwd
        commands["mkdir"] = Mkdir.mkdir
        commands["grep"] =Grep.grep
        commands["wc"]=Wc.wc
        commands["chmod"]=Chmod.chmod
        commands["sort"]=Sort.sort
        commands["history"]=History.history
        commands["historybynum"]=Historybynum.historybynum
        commands["c"]=C.c
        result = commands[cmd](params=params, flags=flags, ispiping=ispiping) # accessing the value of dictionary by key,which calls method in our case
        return result

    def exists(self, cmd):                # A method to check if given command is present in our list
        return cmd in self.commands
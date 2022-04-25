from asyncio import threads
from dataclasses import dataclass
from sys import argv
import sys
import threading
import unittest
import threading
import time
import copy
import json
from memory import creatememory
from gen_inst import RandInstructions
from collections.abc import MutableMapping
from random import randint
import random
from display_help import *
from helper import *

''' Creating a local memory,to keep updating until the program finishes
and then pushes all the updated data into the memory.json '''

class handle_memory:

    def __init__(self):
        self.memory = {}
        for section in range(3):
            section = str(chr(section + 65))
            self.memory[section] = {}
            for i in range(100, 255, 5):
                r = random.randint(1,9)
                self.memory[section][i] = r
        # CREATING INITIAL MEMORY DUMP FILE
        with open("memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)
    
    # METHOD TO UPDATE LOCAL MEMORY DICTIONARY        
    def updatelocalmemory(self,place,value):
        block = place[:1]
        location = place[1:]
        self.memory[block][int(location)] = value

    # METHOD TO FETCH VALUE FOR READ'S
    def readfrommemory(self,loc):
        block = loc[:1]
        location = loc[1:]
        return self.memory[block][int(location)]

    def localmemory(self):
        return self.memory

class Cpu:
    def __init__(self, registers):
        self.cache = []
        self.pc = 0
        self.registers = registers
        self.alu = Alu(registers)

    def loadProcess(self, pcb):
        pass

    def __str__(self):
        return f"[{self.registers}{self.alu}]"


def create_instr(instr,numofwriters):
    a=False
    listofinst = []
    if instr == "local":
        a = True
    elif instr == "nonlocal":
        a = False
    for i in range(1,int(numofwriters)+1):
        ri = RandInstructions(keepInstLocal=a,outFile="writer"+str(i)+".json",isReader = False)
        listofinst.append(ri.getList())
    for i in range(1,(int(numofwriters)*5)+1):
        ri = RandInstructions(keepInstLocal=a,outFile="reader"+str(i)+".json",isReader = True)
        listofinst.append(ri.getList())
    return listofinst


if __name__ == '__main__':
    if len(sys.argv[:])<3:
        print("Incorrect usage...")
        print("Please enter no of Writers,local/nonlocal for instruction preference...\n")
        print("Example : python main.py 5 local\n")
    else:
        l = handle_memory()
        m = l.localmemory()
        with open("memory.json") as f:
            dataf = json.load(f)
        layout = make_layout()
        layout["header"].update(Header())
        layout["side"].update(Panel(loaddata_to_table(dataf," BEFORE"), border_style="#00FF00"))
        layout["body"].update(Panel(loaddata_to_table(dataf," AFTER"), border_style="#00FF00"))

        # with Live(layout, screen=True, redirect_stderr=False) as live:
        #     try:
        #         while True:
        #             sleep(0)
        #     except KeyboardInterrupt:
        # #         pass
        
        # with Live(layout, screen=True, redirect_stderr=False) as live:
        #     try:
                
        no_of_writers = sys.argv[1]
        instr_pref = sys.argv[2] 

        # CREATE INSTRUCTION FILES
        all_instr = create_instr(instr_pref,no_of_writers)

        # CREATE SHARED MEMORY + A LOCAL COPY(DICTIONARY) OF THE SAME
        rw_lock = RWLock()
        threads = []

        reg = Registers(2)
        cpu = Cpu(reg)
        #print(m)
        threads.append(Writer(rw_lock,0,1,all_instr[0],l,m,reg,cpu,1))
        threads.append(Reader(rw_lock,0.1,0.2,all_instr[2],l,m,reg,cpu,1))
        threads.append(Writer(rw_lock,0.2,0.1,all_instr[1],l,m,reg,cpu,2))
        threads.append(Reader(rw_lock,0.3,0,all_instr[3],l,m,reg,cpu,2))
        threads.append(Reader(rw_lock,0.4,0.1,all_instr[4],l,m,reg,cpu,3))
        #threads.append(Reader(rw_lock,0,0,all_instr[2],l,m,reg,cpu))
        for t in threads:
            a = t.run()
            l = a

        with open("memory.json", "w") as f:
            json.dump(l.localmemory(), f, indent=2)
        with open("memory.json") as f:
            data = json.load(f)
        
        layout["body"].update(Panel(loaddata_to_table2(dataf,data," AFTER"), border_style="#00FF00"))
        input("Enter")
            # except KeyboardInterrupt:
            #     pass

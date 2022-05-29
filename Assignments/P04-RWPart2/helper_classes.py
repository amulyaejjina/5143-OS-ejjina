''' --------------------------------------------------------------------------
helper_classes
A collection of helper classes needed for the main program to run

CLASSES PRESENT IN THIS -
1) RWLock       - Synchronization lock class for readers and writers
2) _LightSwitch - An auxiliary "light switch" like object. 
                  The first thread turns on the switch,the last one turns it off
3) Registers    - Represents a set of registers in an overloaded OOP fashion.
4) Register     - Represents a single `register` with a read and write method
                  to change the registers values
5) Alu          - Responsible for performing operations using register data
6) Writer       - An important class,which uses cpu and registers to perform
                  instructions sets
7) Scheduler    - This class will be responsible for scheduling processes
                  using a round robin scheduling algorithm.(NOT USED IN P04,USED SYSTEM THREADS)
------------------------------------------------------------------------------
'''

from asyncio import threads
from cProfile import run
from dataclasses import dataclass
from itertools import count
from pickletools import read_uint2
from sys import argv
import sys
import threading
import time
import json
from numpy import empty
from gen_inst import RandInstructions
from collections.abc import MutableMapping
from random import randint
import random
from rich.panel import Panel
from decimal import Decimal
import time
from collections.abc import MutableMapping
from gen_inst import *
import decimal
from clock import *
from Pcb import *
from Queue import *
from cpu_singleton import *
from lock import *
from display_help import *

'''Global parameters Declaration'''
blah=''
rownum=0
waittimes=[]
instr_len = 0
privileged_order = 0
         

'''
Author for RWLock,_LightSwitch classes = "Mateusz Kobos"
source = "https://code.activestate.com/recipes/577803-reader-writer-lock-with-priority-for-writers/"

A Reader Writer Synchronization lock used in a solution of readers-writers problem. 
In this problem, many readers can simultaneously 
    access a share, and a writer has an exclusive access to this share.
    Additionally, the following constraints should be met: 
    1) no reader should be kept waiting if the share is currently opened for 
        reading unless a writer is also waiting for the share, 
    2) no writer should be kept waiting for the share longer than absolutely 
        necessary.
This class provides following methods to achieve the above - 
    1) reader_acquire()
    2) reader_release()
    3) writer_acquire()
    4) writer_release()

'''
class RWLock:
    """
    The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7] 
    with a modification -- adding an additional lock (C{self.__readers_queue})
    -- in accordance with [2].
    """
    
    def __init__(self):
        self.__read_switch = _LightSwitch()
        self.__write_switch = _LightSwitch()
        self.__no_readers = threading.Lock()
        self.__no_writers = threading.Lock()
        self.__readers_queue = threading.Lock()
        """A lock giving an even higher priority to the writer in certain
        cases (see [2] for a discussion)"""
    
    def reader_acquire(self):
        self.__readers_queue.acquire()
        self.__no_readers.acquire()
        self.__read_switch.acquire(self.__no_writers)
        self.__no_readers.release()
        self.__readers_queue.release()
    
    def reader_release(self):
        self.__read_switch.release(self.__no_writers)
    
    def writer_acquire(self):
        self.__write_switch.acquire(self.__no_readers)
        self.__no_writers.acquire()
    
    def writer_release(self):
        self.__no_writers.release()
        self.__write_switch.release(self.__no_readers)

'''
An auxiliary "light switch"-like object. The first thread turns on the 
    "switch", the last one turns it off).
'''
class _LightSwitch:
    
    def __init__(self):
        self.__counter = 0
        self.__mutex = threading.Lock()
    
    def acquire(self, lock):
        self.__mutex.acquire()
        self.__counter += 1
        if self.__counter == 1:
            lock.acquire()
        self.__mutex.release()

    def release(self, lock):
        self.__mutex.acquire()
        self.__counter -= 1
        if self.__counter == 0:
            lock.release()
        self.__mutex.release()


'''
CREATE INSTRUCTION FILES
This creates a list of instuctions which contains 
all writer lists and reader lists.
Example: 
all_instr = [[Writer 1 all 100 instr],
                [Writer 2 all 100 instr],
                [Reader 1 all 100 instr], 
                [Reader 2 all 100 instr], ...]
'''
def create_instr_new(instr,numofwriters):
    a=False
    listofinst = []
    if instr == "local":
        a = True
    elif instr == "nonlocal":
        a = False
    for i in range(1,int(numofwriters)+1):
        ri = RandInstructions(keepInstLocal=a,outFile="writer"+str(i)+".json",isReader = False)
        listofinst.append(ri.getList())

    return listofinst  

'''
Author for Registers,Register classes = "Dr.Terry Griffin"
source = "https://github.com/rugbyprof/5143-Operating-Systems/tree/master/Assignments/05-P04 "

Class Register - Represents a single `register` with a read and write method
to change the registers values.
'''
class Register:

    def __init__(self):
        """Constructor"""
        self.contents = 0

    def write(self, x):
        """Change value of register"""
        self.contents = x

    def read(self):
        """Return value of register"""
        return self.contents

    def __str__(self):
        """Print out instance in readable format"""
        return f"[{self.contents}]"

    def __repr__(self):
        """Same as __str__"""
        return self.__str__()


'''
Class Registers - Represents a set of registers in an overloaded OOP fashion that
    allows for assignments to go like:

                r = Registers()
                r[0] = 44
                r[1] = 33
'''
class Registers(MutableMapping):
    def __init__(self, num=2):
        """Constructor"""
        self.num = num
        self.registers = []
        for i in range(num):
            self.registers.append(Register())

    def __setitem__(self, k, v):
        """Assigns a value to a particular register as long as the key is
        integer, and within bounds.
        """
        if isinstance(k, int) and k < self.num:
            # setattr(self, self.registers[k], v)
            self.registers[k].write(v)

    def __getitem__(self, k):
        """Returns a value from a specific register indexed by `k`"""
        if isinstance(k, int) and k < self.num:
            # getattr(self, k)
            return self.registers[k].read()
        return None

    def __len__(self):
        """Len() of object instance. Must be here to overload class
        instance or python chokes.
        """
        return self.num

    def __delitem__(self, k):
        """Overloads the del keyword to delete something out of a
        list or dictionary.
        """
        if isinstance(k, int):
            self.registers[k] = None

    def __iter__(self):
        """Allows object iteration, or looping over this object"""
        yield self.registers

    def __str__(self):
        s = "[ "
        i = 0
        for r in self.registers:
            s += f"R{i}{str(r)} "
            i += 1
        return s + "]"

    def __repr__(self):
        return self.__str__()

'''
Class Cpu - Sends in the register data to the alu for opertaions
'''
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

def add(l, r):
    return l + r


def sub(l, r):
    return l - r


def mul(l, r):
    return round(l * r,2)


def div(l, r):
    if r != 0:
        return round(l/r, 2)
    else:
        return 0

def order_privileged_instr(all_instrs_of_writers):
    for i in range(len( all_instrs_of_writers)):
                index = 0
                priorities={}
                for eachset_index in range(len(all_instrs_of_writers[i])):
                    #if any('LOAD' in s for s in all_instrs_of_writers[i][eachset_index]):
                    for s in all_instrs_of_writers[i][eachset_index]:
                        if 'LOAD' and 'R4' in s.split():
                            priorities[eachset_index] = int(s.split()[1])

                sorted_priorities = sorted(priorities.items(), key=lambda x: x[1]) 

                for k in sorted_priorities:

                    all_instrs_of_writers[i].insert(index,all_instrs_of_writers[i][k[0]])
                    all_instrs_of_writers[i].pop(k[0]+1)
                    index = index + 1 
    return all_instrs_of_writers

'''
Class Alu - Responsible for performing operations
'''
class Alu(object):
    def __init__(self, registers):
        self.lhs = None
        self.rhs = None
        self.op = None
        self.registers = registers
        self.ops = {"ADD": add, "SUB": sub, "MUL": mul, "DIV": div}

    def exec(self, op):
        self.lhs = self.registers[0]
        self.rhs = self.registers[1]
        self.op = op.upper()
        ans = self.ops[self.op](self.lhs, self.rhs)
        if self.op == 'DIV' and ans == 0:
            pass
        else:
            self.registers[0] = round(ans,2)
        return self.registers

    def __str__(self):
        return f"{self.lhs} {self.op} {self.rhs}"


'''
Class Writer  - An important class,which uses cpu and registers to perform
                instructions sets
This class is responsible for - 
1) Acquiring lock for critical section
2) throwing in random sleeps before and after loack acquire and release
3) keeping register 4 updated with privileged counter
4) triggering alu to get the operation done and get back the result
'''
class Writer(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.__instructions = kwargs.get("instr", None)
        self.__memoryobject = kwargs.get("memoryobject", None)
        self.__registers = kwargs.get("reg", None)
        self.__num = kwargs.get("num", None)
        self.numofwriters = kwargs.get("numofwriters",0)
        self.lockslist =  kwargs.get("lock", None)
        if len(self.lockslist) == 1:
            self.__rw_lock = self.lockslist[0]
        self.__init_sleep_time = kwargs.get("init_sleep_time",None)
        self.__lock_pref = kwargs.get("lock_pref",None)
        self.layout = kwargs.get("layout", None)
        self.display = Helper_methods()
        self.noofinstr = kwargs.get("noofinstr",0)
        with open("mem_initial.json") as f:
            self.initial_data = json.load(f) 
        self.layout["side"].update(Panel(self.display.loaddata_to_table(self.initial_data," BEFORE"), border_style="#00FF00"))
               

    def run(self):
        global privileged_order
        global blah
        global rownum
        increaseone = False
        for eachset in self.__instructions:
            
            if self.__lock_pref == 'l':
                # print("-----------------------------")
                isPrivileged = False
                increaseone = False
                PIC = -1
                if any('LOAD' in s for s in eachset):
                    isPrivileged = True
                
                if isPrivileged:
                    
                    for line in eachset:
                        if line.startswith("LOAD") and line.endswith("R4"):
                            PIC = line.split()[1]
                            break
                
                    while True:
                        if int(privileged_order) == int(PIC):
                            #privileged_order = privileged_order+1
                            increaseone = True
                            #print("Priviliged section active,executing sequence : " + str(privileged_order))
                            blah = blah + "Priviliged section active,executing sequence : " + str(privileged_order)+'\n'
                            self.layout["side"].update(Panel(blah, border_style="#00FF00"))
                            
                            break
                        #print("Privileged section found,but waiting for its sequence...")
                        blah = blah + "Privileged section found,but waiting for its sequence..."+'\n'
                        self.layout["side"].update(Panel(blah, border_style="#00FF00"))
                        time.sleep(2)

            time.sleep(random.random())
            #time.sleep(self.__init_sleep_time)

            # ACQUIRE LOCK
            if str(self.__lock_pref) == 'l':
                self.lockwaittime_start = time.time()
                self.__rw_lock.writer_acquire()
                self.lockwaittime_end = time.time() - self.lockwaittime_start
            if increaseone:
                privileged_order = privileged_order+1
            counter = 0
            for eachline in eachset:
                
                if(eachline.startswith("LOAD") and eachline.endswith("R4")):
                    counter = counter +1
                    
                    if counter > 1:
                        privileged_order = privileged_order+1

                eachline = eachline.strip().split()
                rownum = rownum + 1
                if (rownum == 34):
                    blah = ""
                    rownum = 0
                if eachline[0] == "LOAD":
                    # Example : "LOAD 1 R3"
                    
                    self.__registers[int(eachline[2].strip()[1:])] = int(eachline[1])
                elif eachline[0] == 'sleep':
                    blah = blah +str(eachline) + " - WRITER " + str(self.__num) +"SLEEPING..."+'\n'
                    self.layout["side"].update(Panel(blah, border_style="#00FF00"))
                     
                elif eachline[0] == "READ":
                    # Example : "READ B195 R2"
                    readvalue = self.__memoryobject.readfrommemory(eachline[1])
                    
                    #print( str(eachline) + " - Writer " + str(self.__num) +" :Read from "+ str(eachline[1]) + " a value of "+ str(readvalue))
 
                    blah = blah +str(eachline) + " - Writer " + str(self.__num) +" :Read from "+ str(eachline[1]) + " a value of "+ str(readvalue)+'\n'
                    self.layout["side"].update(Panel(blah, border_style="#00FF00"))
                        
                    if eachline[2] == 'R1':
                        self.__registers[0] = readvalue
                    else:
                        self.__registers[1] = readvalue
                    
                elif eachline[0] in ["ADD", "SUB", "MUL", "DIV"]:
                    # Example : #   "ADD R2 R1"
                    alu = Alu(self.__registers)
                    #print(str(eachline) + " - Writer" + str(self.__num) +" performed operation")
                    blah = blah +str(eachline) + " - Writer" + str(self.__num) +" performed operation"+'\n'
                    self.layout["side"].update(Panel(blah, border_style="#00FF00"))
                      
                    if eachline[0] == 'ADD':
                        self.__registers = alu.exec('add')
                    if eachline[0] == 'MUL':
                        self.__registers = alu.exec("mul")
                    if eachline[0] == 'SUB':
                        self.__registers = alu.exec("sub")
                    if eachline[0] == 'DIV':
                        self.__registers = alu.exec("div")

                elif eachline[0] == "WRITE":
                    # Example : "WRITE R1 A105"
                    
                    self.__memoryobject.updatelocalmemory(eachline[2],self.__registers[0])
                    #print(str(eachline) + " - Writer " + str(self.__num) +" :Wrote to "+ str(eachline[2]) + " a value of "+ str(self.__registers[0]))
                    blah = blah +str(eachline) + " - Writer " + str(self.__num) +" :Wrote to "+ str(eachline[2]) + " a value of "+ str(self.__registers[0])+'\n'
                    self.layout["side"].update(Panel(blah, border_style="#00FF00"))
                    
                    with open("memory.json", "w") as f:
                        json.dump(self.__memoryobject.localmemory(), f, indent=2)
                    with open("memory.json") as f:
                        updating_data = json.load(f) 
                    self.layout["body"].update(Panel(self.display.loaddata_to_table2(self.initial_data,updating_data," AS IT'S CHANGING..."), border_style="#00FF00"))
                # elif eachline[0] == "sleep":
                #     blah = blah + "Writer"+ self.__num+" sleeping..."
                #     self.layout["side"].update(Panel(blah, border_style="#00FF00"))
                #     #time.sleep(int(eachline[1]))
                    
                #     overalltask.update(task_id, advance=(1/(int(self.numofwriters)*100))*100)
            #print('\n')

            # RELEASE LOCK
            if str(self.__lock_pref) == 'l':
                self.__rw_lock.writer_release()
                blah = blah + '------------------------------------------------'+'\n'
                self.layout["side"].update(Panel(blah, border_style="#00FF00"))
            blah = blah +'\n'
            self.layout["side"].update(Panel(blah, border_style="#00FF00"))    
            time.sleep(random.random())
            #time.sleep(self.__init_sleep_time)
            overalltask.update(task_id, advance = (1/int(self.noofinstr))*100)

def create_pcbs(no_of_writers,instructions):
    pcb_list=[]

    for i in range(no_of_writers):
        pcb_list.append(Pcb(instructions = instructions[i],processid= i+1))
    return pcb_list

def isfoundinWaitQueue(waitqueue,pid):
    for item in waitqueue.allitems():
        if int(pid) == int(item.processid):
            return True

def findtotal(all_instr):
    count=0
    for item in all_instr:
        for each in all_instr[item]:
            count = count+1
    return count

'''
Class Scheduler - This class will be responsible for scheduling processes
using a round robin scheduling algorithm.

THIS CLASS IS NOT USED IN P04 BUT THIS WORKS...
'''
class Scheduler():
    def __init__(self, **kwargs):
        self.timeslice = kwargs.get("slice", None)
        self.pcblist = kwargs.get("pcbs", None)
        self.registers = kwargs.get("reg", None)
        self.numprocesses = kwargs.get("numprocesses", None)
        self.memoryobject = kwargs.get("memoryobject", None)
        self.registers = kwargs.get("registers", None)
        self.timeslicecheck = kwargs.get("slice", None)
        self.readyQueue = kwargs.get("readyQ", None)
        self.waitQueue = kwargs.get("waitQ", None)
        self.CPU = Cpu_singleton()
        # add incoming pcbs to ready queue
        self.readyQueue = Queue()
        self.waitQueue = Queue()
        for pcb in self.pcblist:
            self.readyQueue.add(pcb)
        self.readyQueue.print()
  
    def run(self):
        A = Clock.getInstance()
        self.timeslicecheck = self.timeslice
        if not self.CPU.isbusy():
            if not self.readyQueue.empty():
                self.CPU.run_process(self.readyQueue.first())
                self.readyQueue.remove()
            running_pcb_cpu = self.CPU.running_process
            index = 0
            global instr_len
            instr_len = len(running_pcb_cpu.instr_clubbed)
            while instr_len != 0:
                instr_len = instr_len - 1
                eachline = running_pcb_cpu.instr_clubbed[index]

                completed_sleep_pcb = -1
                index_of_completed=-1
                if not self.waitQueue.empty():
                    for item in range(len(self.waitQueue.allitems())):
                        if self.waitQueue.allitems()[item].sleeptime != 0:
                            self.waitQueue.allitems()[item].sleeptime = self.waitQueue.allitems()[item].sleeptime-1
                        elif self.waitQueue.allitems()[item].sleeptime == 0:
                            completed_sleep_pcb = self.waitQueue.allitems()[item]
                            self.waitQueue.remove_at_index(item)
                            break
                if completed_sleep_pcb != -1:           
                    for i in range(self.readyQueue.length()):
                        if self.readyQueue.allitems()[i] == completed_sleep_pcb:
                            index_of_completed = i
                            break
                if index_of_completed != -1:
                    print("Sleep completed,.bring back...")
                    self.readyQueue.add(running_pcb_cpu) # R = 2,1
                    self.CPU.remove_process() 
                    self.CPU.run_process(completed_sleep_pcb)
                    self.readyQueue.remove_at_index(index_of_completed)
                    running_pcb_cpu = self.CPU.running_process
                    instr_len = len(running_pcb_cpu.instr_clubbed)
                    index = 0

                
                if (A.clock == 7) :
                    A.clock=0
                    self.readyQueue.add(running_pcb_cpu) # R = 2,1
                    self.CPU.remove_process() # CPU = empty
                    self.CPU.run_process(self.readyQueue.first()) # CPU = 2
                    self.readyQueue.remove()
                    running_pcb_cpu = self.CPU.running_process
                    instr_len = len(running_pcb_cpu.instr_clubbed)
                    index = 0
                    print("Switching after 7 clocks...")
                    continue
                else:
                    found_in_wQ = False
                    eachline = eachline.strip().split()
                    if eachline[0] == "sleep" or isfoundinWaitQueue(self.waitQueue,running_pcb_cpu.processid):
                        
                        print(" Writer " + str(running_pcb_cpu.processid) + "SLEEPING...")
                        #time.sleep(int(eachline[1]))
                        self.readyQueue.add(running_pcb_cpu)
                        for item in self.waitQueue.allitems():
                            if int(running_pcb_cpu.processid) == int(item.processid):
                                found_in_wQ = True
                        if not found_in_wQ:
                            print("Adding to wait queue...")
                            self.waitQueue.add(running_pcb_cpu)
                        if not isfoundinWaitQueue(self.waitQueue,running_pcb_cpu.processid):
                            running_pcb_cpu.sleeptime = int(eachline[1])

                            updated_list = running_pcb_cpu.instr_clubbed
                            updated_list.pop(0)
                            running_pcb_cpu.instr_clubbed = updated_list
                        self.CPU.remove_process() # CPU = empty
                        if not self.readyQueue.empty():
                            self.CPU.run_process(self.readyQueue.first()) # CPU = 2
                            self.readyQueue.remove()
                        running_pcb_cpu = self.CPU.running_process
                        instr_len = len(running_pcb_cpu.instr_clubbed)
                        index = 0
                        continue
                    elif eachline[0] == "READ":
                        # Example : "READ B195 R2"
                        readvalue = self.memoryobject.readfrommemory(eachline[1])
                        
                        print( str(eachline) + " - Writer " + str(running_pcb_cpu.processid) +" :Read from "+ str(eachline[1]) + " a value of "+ str(readvalue))
                        if eachline[2] == 'R1':
                            self.registers[0] = readvalue
                        else:
                            self.registers[1] = readvalue
                        
                    elif eachline[0] in ["ADD", "SUB", "MUL", "DIV"]:
                        # Example : #   "ADD R2 R1"
                        alu = Alu(self.registers)
                        print(str(eachline) + " - Writer" + str(running_pcb_cpu.processid) +" performed operation")
                        if eachline[0] == 'ADD':
                            self.registers = alu.exec('add')
                        if eachline[0] == 'MUL':
                            self.registers = alu.exec("mul")
                        if eachline[0] == 'SUB':
                            self.registers = alu.exec("sub")
                        if eachline[0] == 'DIV':
                            self.registers = alu.exec("div")

                    elif eachline[0] == "WRITE":
                        # Example : "WRITE R1 A105"
                        
                        self.memoryobject.updatelocalmemory(eachline[2],self.registers[0])
                        print(str(eachline) + " - Writer " + str(running_pcb_cpu.processid) +" :Wrote to "+ str(eachline[2]) + " a value of "+ str(self.registers[0])+'\n')
                        with open("memory.json", "w") as f:
                            json.dump(self.memoryobject.localmemory(), f, indent=2)

                    elif eachline[0] == "LOAD":
                        # Example : "LOAD 1 R3"
                        print("Priviliged section update :: " , eachline)
                        self.registers[int(eachline[2].strip()[1:])] = int(eachline[1])
                    

                    A.clock = A.clock+1
                updated_list = running_pcb_cpu.instr_clubbed
                updated_list.pop(0)
                running_pcb_cpu.instr_clubbed = updated_list
                if instr_len == 0:
                    A.clock=0
                    self.CPU.remove_process() # CPU = empty
                    if not self.readyQueue.empty():
                        self.CPU.run_process(self.readyQueue.first()) # CPU = 2
                        self.readyQueue.remove()
                        running_pcb_cpu = self.CPU.running_process
                    instr_len = len(running_pcb_cpu.instr_clubbed)
                    index = 0
                    print("Switching...c")
                    print("After switching Ready Queue-----")
                    for item in self.readyQueue.allitems():
                        print(item.processid)
                print("Current Wait Queue-------")
                print(self.waitQueue.allitems())

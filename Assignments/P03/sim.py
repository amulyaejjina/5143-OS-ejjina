#!/usr/bin/env python3
'''
----------------------------------------------------------------------------------------------------------
                        CPU SCHEDULING SIMULTAION

DESCRIPTION : The below program mimics the CPU scheduling of processes by using a bunch of 
scheduling algorithms.

AIM OF THE PROJECT : To find out the wait times - CPU WaitTime,IO Wait Time
and maximize throughput ,minimize wait times

DETAILED DESCRIPTION OF THE APPROACH : This project tries to simulate a real world CPU processing starting with
1) Sends in an input file to the simulator with a number of process having the following data per process- 
    0 1 p2 9 14 12 14 9 14 9 14 12 15 9,the adjacent numbers in words respectively are as below - 
    Arrival Time, Process ID, Priority, CPUBurst1, IOBurst1, CPUBurst2, IOBurst2, CPUBurst3, IOBurst3 ....

2) The simulator/driver program fires up a clock which is nothing but a variable implemented in singleton pattern
and reads in the processes based on the arrival times against the clock.

3) The incoming processes are put into respective Queues - 
We have followed a Five State pattern i.e.
    NEW
    READY
    RUNNING
    WAITING
    IO (JUST TO REPRESENT THAT THE PROCESS IS BEING SERVED IN IO SIMILAR TO RUNNING QUEUE)
    TERMINATED

4) Algorithms come into picture when choosing processes to place into CPU resource.

5) Based on the algorithm the processes are executed(decrease in burst times)

6) Once a process has completed its burst times aka its purpose to come into system(opening a file and writing could be a process)
it will be terminated and the wait times are measured.

SCHEDULING ALGORITHMS USED : First come first serve,Round Robin,Shortest Job first,
                             Shortest Time remaining first,Priority Scheduling(pre-emption)
DESIGN PATTERNS USED : SINGLETON for Clock class,CPU class,IO class
-----------------------------------------------------------------------------------------------------------
'''
from termcolor import colored
#from pyfiglet import Figlet
from calendar import c
from mailbox import linesep
from os import read
from tkinter.ttk import Progressbar
from webbrowser import get
from time import sleep
import sys
from tkinter import *
from random import randint
from tkinter import ttk
from Queue import *
from Cpu_singleton import *
from Io_singleton import *
from Clock import *
from Pcb import *
from datetime import datetime
from time import sleep
from rich import *
import sys,os
import time
from rich.live import Live
from rich.table import Table
from datetime import datetime
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from display_helper import *
from time import sleep
from rich.markdown import Markdown
import t as kintergraph

'''
Declaration of all the Queues and necessary variables
'''
pcb_dict={}
newQueue = Queue()
readyQueue=Queue()
runningQueue=Queue()
waitingQueue=Queue()
iOQueue=Queue()
terminatedQueue=Queue()
pcb_list=[]
cpu_resource=[]
cpu_list=[]
io_list=[]
# time_slice = 8
# time_slice_check = 17
process_data = ""
cpu_id = 0


def algorithms(cpu,algo):
    a={
        'srf':srf(),
        'sjf':sjf(),
        'pp':pp()
    }
    if algo == "fcfs" or algo == "rr":
        cpu.run_process(readyQueue.first())
        readyQueue.remove()
    else:
        cpu.run_process(a[algo])
        readyQueue.remove_at(a[algo])



def scheduler(length,type,cpus,ios,slice):
    #B = Buffer()
    global process_data
    A = Clock.getInstance()
    time_slice_check = slice
    create_cpus_ios(cpus,ios)
    term_proc=1
    # f = open('output.txt', 'r+')
    # f.truncate(0) # need '0' when using r+
    row = 0
    layout = make_layout()
    layout["header"].update(Header())
    layout["body"].update(Panel(process_data, border_style="#00FF00"))
    layout["IOs"].update(Panel(ioFunction(ios,None,0,""), border_style="#00FF00"))
    layout["CPUs"].update(Panel(cpuFunction(cpus,None,0,""), border_style="#00FF00"))
    layout["footer1"].update(Panel(progress_table, border_style="#00FF00",title="[b]OVERALL PROGRESS[b]",))
    layout["footer2"].update(Panel(meth(0,0,0), border_style="#00FF00"))
        
    with Live(layout, refresh_per_second=4, screen=True,transient=False) as live:
        rownum = 0
        while(term_proc<=length):
            
            # If IO is busy,decrement io burst time of running process in io
            moved_in_this_cycle = False
            swapped_pp_in_this_cycle = False
            
            # a = iobusy_activities(io,moved_in_this_cycle)
            # moved_in_this_cycle = a
            for io in io_list:
                if io.isbusy():
                    running_pcb_io = io.running_process
                    if len(running_pcb_io.ioBursts)>1 :
                        if (running_pcb_io.ioBursts[0] == 0):
                            move_to_readyQ(running_pcb_io)
                            running_pcb_io.ioBursts.pop(0)
                            layout["IOs"].update(Panel(ioFunction(ios,io.running_process,int(io.ioid()),"left"), border_style="green"))
                            
                            io.remove_process()

                            if not waitingQueue.empty():
                                io.run_process(waitingQueue.first())
                                layout["IOs"].update(Panel(ioFunction(ios,io.running_process,int(io.ioid()),"enter"), border_style="green"))
                
                                waitingQueue.remove()
                                layout["footer2"].update(Panel(meth(0,0,-1), border_style="#00FF00"))
                                #job_progress.update(waitingtask, advance=waitingQueue.length())
                        else:
                            running_pcb_io.ioBursts[0] = int(running_pcb_io.ioBursts[0])-1

                    elif len(running_pcb_io.ioBursts)==1 and (running_pcb_io.ioBursts[0] == 0):
                        move_to_readyQ(running_pcb_io)
                        running_pcb_io.ioBursts.pop(0)
                        layout["IOs"].update(Panel(ioFunction(ios,io.running_process,int(io.ioid()),"left"), border_style="green"))
                
                        io.remove_process()
                        #layout["IOs"].update(Panel(ioFunction(ios,io.running_process,int(io.ioid()),"left"), border_style="green"))
                
                        layout["footer2"].update(Panel(meth(0,1,0), border_style="#00FF00"))
                        #layout["footer2"].update(Panel(meth(0,int(newQueue.length()),1,int(readyQueue.length()),0,int(waitingQueue.length())), border_style="#00FF00"))

                        #job_progress.update(iotask, advance=-1)
                        moved_in_this_cycle=True
                    
                    elif len(running_pcb_io.ioBursts)==1 and (running_pcb_io.ioBursts[0] != 0):
                        running_pcb_io.ioBursts[0] = int(running_pcb_io.ioBursts[0])-1

        # Check IO availability,push from WAITING --> IO
            if  (ios == 1 and not io_list[0].isbusy()) or (ios ==2 and (not io_list[0].isbusy() or not io_list[1].isbusy())) or (ios == 3 and  (not io_list[0].isbusy() or not io_list[1].isbusy() or not io_list[2].isbusy())):
        # if not io.isbusy():
                for each_io in io_list:
                    if not each_io.isbusy():
                        if not waitingQueue.empty():
                            each_io.run_process(waitingQueue.first())
                            layout["IOs"].update(Panel(ioFunction(ios,each_io.running_process,int(each_io.ioid()),"entered"), border_style="green"))
                
                            waitingQueue.remove()
                            layout["footer2"].update(Panel(meth(0,0,-1), border_style="#00FF00"))
                            #layout["footer2"].update(Panel(meth(0,int(newQueue.length()),0,int(readyQueue.length()),-1,int(waitingQueue.length())), border_style="#00FF00"))
                              
                            #job_progress.update(waitingtask, advance=waitingQueue.length())
                            io_flag = True

            # Increasing IOWaitTime for any processes remaining in WAITING Queue
            if not waitingQueue.empty():
                if (ios == 1 and io_list[0].isbusy()) or  (ios == 2 and io_list[0].isbusy() and io_list[1].isbusy()) or (ios == 3 and io_list[0].isbusy() and io_list[1].isbusy() and io_list[2].isbusy()):
                    for item in waitingQueue.allitems():
                        item.IOWaittime = item.IOWaittime +1
                #layout["footer2"].update(Panel(meth(4,0,-1), border_style="#00FF00"))
                                   
            # If CPU is busy,decrement cpu burst time of running process in cpu
            # for cpu in cpus:
            if (cpus == 1 and cpu_list[0].isbusy()) or (cpus == 2 and (cpu_list[0].isbusy() or cpu_list[1].isbusy())) or (cpus == 3 and (cpu_list[0].isbusy() or cpu_list[1].isbusy() or cpu_list[2].isbusy())):
            # if cpu.isbusy():
                for cpu in cpu_list:
                    if cpu.isbusy():
                    # print(cpu)
                        running_pcb_cpu = cpu.running_process
                        # print(running_pcb_cpu)

                        if len(running_pcb_cpu.cpuBursts)>1:
                            if(running_pcb_cpu.cpuBursts[0] == 0):
                                if type == 'rr':
                                    time_slice_check = slice
                                move_to_waitingQ(running_pcb_cpu)
                                layout["footer2"].update(Panel(meth(0,0,1), border_style="#00FF00"))
                                #layout["footer2"].update(Panel(meth(0,int(newQueue.length()),0,int(readyQueue.length()),1,int(waitingQueue.length())), border_style="#00FF00"))

                                running_pcb_cpu.cpuBursts.pop(0)
                                layout["CPUs"].update(Panel(cpuFunction(cpus,cpu.running_process,int(cpu.cpuid()),"left"), border_style="green"))
                
                                cpu.remove_process()
                                
                                #job_progress.update(runningtask, advance=-1)
                                if not readyQueue.empty():
                                    algorithms(cpu,type)
                                    layout["footer2"].update(Panel(meth(0,-1,0), border_style="#00FF00"))
                                    #layout["footer2"].update(Panel(meth(0,int(newQueue.length()),-1,int(readyQueue.length()),0,int(waitingQueue.length())), border_style="#00FF00"))

                                    layout["CPUs"].update(Panel(cpuFunction(cpus,cpu.running_process,int(cpu.cpuid()),"enter"), border_style="green"))
                    
                                    
                            elif type == "pp":
                                if not readyQueue.empty():
                                    running_process_pri = running_pcb_cpu.priority[1]
                                    ready_q_highest_pri = pp().priority[1]
                                    if(ready_q_highest_pri < running_process_pri):
                                        move_to_readyQ(running_pcb_cpu)
                                        layout["CPUs"].update(Panel(cpuFunction(cpus,cpu.running_process,int(cpu.cpuid()),"left"), border_style="green"))
                                        layout["footer2"].update(Panel(meth(0,1,0), border_style="#00FF00"))
                                        #layout["footer2"].update(Panel(meth(0,int(newQueue.lenght()),1,int(readyQueue.length()),0,int(waitingQueue.length())), border_style="#00FF00"))

                                        cpu.remove_process()
                                        cpu.run_process(pp())
                                        layout["CPUs"].update(Panel(cpuFunction(cpus,cpu.running_process,int(cpu.cpuid()),"enter"), border_style="green"))
                
                                        readyQueue.remove_at(pp())
                                        layout["footer2"].update(Panel(meth(0,-1,0), border_style="#00FF00"))
                                        #layout["footer2"].update(Panel(meth(0,int(newQueue.length()),-1,int(readyQueue.length()),0,int(waitingQueue.length())), border_style="#00FF00"))

                                        swapped_pp_in_this_cycle = True
                                if not swapped_pp_in_this_cycle:
                                    running_pcb_cpu.cpuBursts[0] = int(running_pcb_cpu.cpuBursts[0])-1
                            elif type == "rr":
                                if time_slice_check == 0:
                                    move_to_readyQ(running_pcb_cpu)
                                    #job_progress.update(readytask, advance=readyQueue.length())
                                    layout["CPUs"].update(Panel(cpuFunction(cpus,cpu.running_process,int(cpu.cpuid()),"left"), border_style="green"))
                                    layout["footer2"].update(Panel(meth(0,1,0), border_style="#00FF00"))
                                    #layout["footer2"].update(Panel(meth(0,int(newQueue.length()),1,int(readyQueue.length()),0,int(waitingQueue.length())), border_style="#00FF00"))

                                    cpu.remove_process()
                                    cpu.run_process(readyQueue.first())
                                    layout["CPUs"].update(Panel(cpuFunction(cpus,cpu.running_process,int(cpu.cpuid()),"enter"), border_style="green"))
                
                                    readyQueue.remove()
                                    layout["footer2"].update(Panel(meth(0,0,-1), border_style="#00FF00"))
                                    #layout["footer2"].update(Panel(meth(0,int(newQueue.length()),0,int(readyQueue.length()),-1,int(waitingQueue.length())), border_style="#00FF00"))

                                    time_slice_check = slice
                                else:
                                    running_pcb_cpu.cpuBursts[0] = int(running_pcb_cpu.cpuBursts[0])-1
                                    time_slice_check=time_slice_check-1
                                    
                            else:
                                running_pcb_cpu.cpuBursts[0] = int(running_pcb_cpu.cpuBursts[0])-1
                        elif len(running_pcb_cpu.cpuBursts)==1 and (running_pcb_cpu.cpuBursts[0] == 0):
                                if type == "rr":
                                    time_slice_check = slice
                                terminate_process()               
                                running_pcb_cpu.cpuBursts.pop(0)
                                f = open('output.txt','a')
                                f.write("Process {} terminated at {} with cpuwaittime - {} , iowaittime - {} , TAT - {}\n".format(running_pcb_cpu.pid,A.clock,running_pcb_cpu.CPUWaittime,running_pcb_cpu.IOWaittime,(running_pcb_cpu.endTime - int(running_pcb_cpu.arrivalTime))))
                                f.close()
                                #B.generate_buffer()
                                time.sleep(0.1)
                                #table.add_row(f"Process {running_pcb_cpu.pid} terminated at {A.clock} clock cycle" ,f"{running_pcb_cpu.CPUWaittime}", f"{running_pcb_cpu.IOWaittime}")
                                #pan(2,1,table)
                                running_pcb_cpu.endTime = A.clock
                                rownum = rownum + 1
                                if (rownum == 29):
                                    process_data = ""
                                    rownum = 0
                                process_data = process_data + f"Process {running_pcb_cpu.pid} terminated at {A.clock} clock cycle with CPUWt : {running_pcb_cpu.CPUWaittime} , IOWt : {running_pcb_cpu.IOWaittime} , TAT : {(int(running_pcb_cpu.endTime) - int(running_pcb_cpu.arrivalTime) )}" +"\n"
                                layout["body"].update(Panel(process_data, border_style="green"))
                                row = row+1
                                overalltask.update(task_id, advance=(1/length)*100)
                                #print("Process {} terminated at {} with cpuwaittime - {} , iowaittime - {}".format(running_pcb_cpu.pid,A.clock,running_pcb_cpu.CPUWaittime,running_pcb_cpu.IOWaittime))
                                
                                layout["CPUs"].update(Panel(cpuFunction(cpus,cpu.running_process,int(cpu.cpuid()),"left"), border_style="green"))
                
                                cpu.remove_process()
                                term_proc = term_proc+1
                                if term_proc == length+1:
                                    avgcpu,avgio,avgtat = get_avg_waittimes_for_display(pcb_dict)
                                    process_data = process_data + "[b]----------------------------------------------------------------[b]" + "\n" +"[b]SIMULATION COMPLETED ✅ [b]\n"+f"The Average CPU Wait time is {avgcpu}\nThe Average IO Wait time is {avgio}\nThe Average TAT time is {avgtat}"+"\n----------------------------------------------------------------"
                                    layout["body"].update(Panel(process_data, border_style="green"))
                                    #layout["footer2"].update(Panel(meth(newQueue.length(),readyQueue.length(),waitingQueue.length()), border_style="#00FF00"))
                                    layout["footer2"].update(Panel(meth(-3,-3,-3), border_style="#00FF00"))
                                    if no_of_cpus == 3:
                                        kintergraph.graph()

                        elif len(running_pcb_cpu.cpuBursts)==1 and (running_pcb_cpu.cpuBursts[0] != 0):
                            running_pcb_cpu.cpuBursts[0] = int(running_pcb_cpu.cpuBursts[0])-1  
                            if type == 'rr':
                                time_slice_check=time_slice_check-1

            # Check CPU availability,push from READY --> CPU
            if  ((cpus == 1 and not cpu_list[0].isbusy()) or (cpus ==2 and (not cpu_list[0].isbusy() or not cpu_list[1].isbusy())) or (cpus ==3 and  (not cpu_list[0].isbusy() or not cpu_list[1].isbusy() or not cpu_list[2].isbusy()))) and not moved_in_this_cycle:
            # if not cpu.isbusy() and not moved_in_this_cycle: 
                for each_cpu in cpu_list:
                    if not each_cpu.isbusy():
                        if not readyQueue.empty():
                            algorithms(each_cpu,type)
                            layout["footer2"].update(Panel(meth(0,-1,0), border_style="#00FF00"))
                            #layout["footer2"].update(Panel(meth(0,int(newQueue.length()),-1,int(readyQueue.length()),0,int(waitingQueue.length())), border_style="#00FF00"))

                            indexNum = each_cpu.cpuid()
                            #time.sleep(0.2)
                            layout["CPUs"].update(Panel(cpuFunction(cpus,each_cpu.running_process,int(indexNum),"enter"), border_style="green"))
                            
                            #time.sleep(0.1)
            # Increasing CPUWaitTime for any processes remaining in READY Queue
            if not readyQueue.empty():
                if (cpus == 1 and cpu_list[0].isbusy()) or  (cpus == 2 and cpu_list[0].isbusy() and cpu_list[1].isbusy()) or (cpus == 3 and cpu_list[0].isbusy() and cpu_list[1].isbusy() and cpu_list[2].isbusy()):
                    for item in readyQueue.allitems():
                        item.CPUWaittime = item.CPUWaittime +1
            
            # Check for any processes in NEW Queue,push them from NEW --> READY
            if not newQueue.empty() and A.clock != 0:
                move_new_to_ready(pcb_dict[str(A.clock-1)])
                newQueue.removeall() # have to remove everything
                layout["footer2"].update(Panel(meth(-(int(newQueue.length())),0,0), border_style="#00FF00")) 
                #layout["footer2"].update(Panel(meth(-(int(newQueue.length())),int(newQueue.length()),0,int(readyQueue.length()),0,int(waitingQueue.length())), border_style="#00FF00"))

                #layout["footer2"].update(Panel(meth(-4,0,-1), border_style="#00FF00"))
                #job_progress.update(newtask, advance=newQueue.length())
            
            # Check for any incoming processes --> Push to NEW Queue
            if newQueue.empty() and str(A.clock) in pcb_dict:
                
                add_to_newqueue(pcb_dict[str(A.clock)])
                layout["footer2"].update(Panel(meth(int(newQueue.length()),0,0), border_style="#00FF00"))
                #layout["footer2"].update(Panel(meth((int(newQueue.length())),int(newQueue.length()),0,int(readyQueue.length()),0,int(waitingQueue.length())), border_style="#00FF00"))

                #layout["footer2"].update(Panel(meth(4,0,-1), border_style="#00FF00"))
                #job_progress.update(newtask, advance=newQueue.length())
        
            # for i in range(len(pcb_dict)):
            #     for item in pcb_dict:
            #         if not item.cpuBursts:
            #             if not item.ioBursts:
            #                 print("Process {} terminated at {}".format(item.pid,A.clock))
            # print("For clock {}".format(A.clock))
            # print("--------------------------------")
            # print("NewQueue - ")
            # for item in newQueue.allitems():
            #     print(item.pid)
            # print("ReadyQueue - ")
            # for item in readyQueue.allitems():
            #     print(item.pid)
            # print("Running Queue / CPU1 - ")
            # #if not cpu.isbusy():
            # if not cpu_list[0].isbusy() :
            #     print("None")
            # else:
            #     print(cpu_list[0].running_process.pid)
            # print("Running Queue / CPU2 - ")
            # if cpu_list[1] is not None and not cpu_list[1].isbusy() :
            #     print("None")
            # else:
            #     print(cpu_list[1].running_process.pid)
            # # if cpu3 is not None and not cpu3.isbusy() :
            # #     print("None")
            # # else:
            # #     print(cpu3.running_process.pid)
            # print("WaitingQueue - ")
            # for item in waitingQueue.allitems():
            #     print(item.pid)
            # print("IO Queue / IO - ")
            # if not io_list[0].isbusy():
            #     print("None")
            # else:
            #     print(io_list[0].running_process.pid)
            # # if io2 is not None and not io2.isbusy() :
            # #     print("None")
            # # else:
            # #     print(io2.running_process.pid)
            # # if io3 is not None and not io3.isbusy() :
            # #     print("None")
            # # else:
            # #     print(io3.running_process.pid)
            # for i in range(len(pcb_dict)):
            #     for item in pcb_dict[str(i)]:
            #         # if len(item.cpuBursts) != 0:
            #         #     if len(item.ioBursts) != 0:
            #                 display(item)
            A.clock = A.clock+1
            if int(A.clock) == 70:
                layout["footer2"].update(Panel(meth(-3,0,0), border_style="#00FF00"))
            #time.sleep(0.05)                          

        print("Simulation is completed ...✅")
        print("The average wait time is ")
        if no_of_cpus == 3:
            kintergraph.graph()
        try:
            while True:
                sleep(0)
        except KeyboardInterrupt:
            pass
#----------------------------------------------------------------------------------------------------

# All methods - 
def create_cpus_ios(cpus,ios):
    if cpus == 1:
        cpu1=Cpu_singleton()
        cpu_list.append(cpu1)
    elif cpus == 2:
        cpu1=Cpu_singleton()
        cpu2=Cpu_singleton2()
        cpu_list.append(cpu1)
        cpu_list.append(cpu2)
    elif cpus == 3:
        cpu1=Cpu_singleton()
        cpu2=Cpu_singleton2()
        cpu3=Cpu_singleton3()
        cpu_list.append(cpu1)
        cpu_list.append(cpu2)
        cpu_list.append(cpu3)

    if ios == 1:
        io1=Io_singleton()
        io_list.append(io1)
    elif ios == 2:
        io1=Io_singleton()
        io2=Io_singleton2()
        io_list.append(io1)
        io_list.append(io2)
    elif ios == 3:
        io1=Io_singleton()
        io2=Io_singleton2()
        io3=Io_singleton3()
        io_list.append(io1)
        io_list.append(io2)
        io_list.append(io3)

def pp():
    min = readyQueue.allitems()[0].priority[1]
    min_process = readyQueue.allitems()[0]
    for item in range(len(readyQueue.allitems())):
        if min > readyQueue.allitems()[item].priority[1]:
            min = readyQueue.allitems()[item].priority[1]
            min_process = readyQueue.allitems()[item]
    return min_process

def Display(pcb):
    # for item in pcb_dict:
        tat = pcb.endTime - int(pcb.arrivalTime)
        #print("Process-" + item.pid + " : CPUWaitTime -" + item.CPUWaittime + ","+ "IOWaitTime -" + item.IOWaittime)
        #print("Process id = {}".format(item.pid))
        return (" Process id = {}, -  CPUWaittime : {} ,IOWaittime : {} ,TAT : {} ".format(pcb.pid,pcb.CPUWaittime,pcb.IOWaittime,tat))
        #print("\n")
def sjf():
    min = readyQueue.allitems()[0].sumofCpuBursts
    min_process = readyQueue.allitems()[0]
    for item in range(len(readyQueue.allitems())):
        if min > readyQueue.allitems()[item].sumofCpuBursts:
            min = readyQueue.allitems()[item].sumofCpuBursts
            min_process = readyQueue.allitems()[item]
    return min_process

def srf():
    for item in range(len(readyQueue.allitems())):
        for i in readyQueue.allitems()[item].cpuBursts:
            readyQueue.allitems()[item].sumofremCpuBursts=readyQueue.allitems()[item].sumofremCpuBursts + int(i)
    min = readyQueue.allitems()[0].sumofremCpuBursts
    min_process = readyQueue.allitems()[0]
    for item in range(len(readyQueue.allitems())):
        if min > readyQueue.allitems()[item].sumofremCpuBursts:
            min = readyQueue.allitems()[item].sumofremCpuBursts
            min_process = readyQueue.allitems()[item]
    return min_process

def terminate_process():
    pass

def move_to_waitingQ(pcb):
    waitingQueue.add(pcb)

def move_to_readyQ(pcb):
    readyQueue.add(pcb)

def move_new_to_ready(list):
    for item in list:
        readyQueue.add(item)
def print_ids(list):
    a = []
    for item in readyQueue.allitems():
        a.append(item.pid)
    return a

def add_to_newqueue(list):
    for item in list:
        newQueue.add(item)


def getprocesses(filename):
    with open(filename) as f:
       p_list = f.readlines()
       return p_list

def display(pcb):
    print("Process id = {}".format(pcb.pid))
    print("     CPUWaittime : {} ,IOWaittime : {} ,cpu bursts : {} ,io bursts : {}".format(pcb.CPUWaittime,pcb.IOWaittime,pcb.cpuBursts,pcb.ioBursts))
    # print("     IOWaittime : {}".format(pcb.IOWaittime))
    # print("     cpu bursts : {}".format(pcb.cpuBursts))
    # print("     io bursts : {}".format(pcb.ioBursts))
    print("\n")

def create_pcbs(input):
    '''Creates a dictionary with arrival times of the processes as keys
        KEY   : ARRIVAL TIME
        VALUE : LIST OF PCB BLOCKS WHICHEVER HAS SAME ARRIVAL TIME
    Sample :
    {
    '0': [pcb1, pcb2],
    '1': pcb3, 
    '2': pcb4
    }
    '''
    for process in input:
        process_split=process.split()
        if process_split[0] not in pcb_dict:
            pcb_dict[process_split[0]] =[]
        pcb_dict[process_split[0]].append(Pcb(process))

def get_avg_waittimes_for_display(pcbdict):
    a=[]
    sum=0
    sum2=0
    avgCPUWaittime=0
    avgIOWaittime=0
    avgtattime=0
    tattime = 0
    for item in pcbdict:
        if len(pcbdict[item])>=1:
            for i in range(len(pcbdict[item])):
                a.append(pcbdict[item][i])
        else:
            a.append((pcbdict[item]))
    for item in a:
        sum=sum+item.CPUWaittime 
        sum2 = sum2+item.IOWaittime
        tat = item.endTime - int(item.arrivalTime)
        tattime = tattime+tat

    avgCPUWaittime = sum/len(a)
    avgIOWaittime = sum2/len(a)
    avgtattime = tattime/len(a)
    return avgCPUWaittime,avgIOWaittime,avgtattime

if __name__ == '__main__':
    no_of_cpus=0
    no_of_ios=0
    type=""
    time_slice_check=0
    #filename = input("Enter input filename: ")
    if len(sys.argv[:])<4:
        print("Incorrect Usage...")
        print("Please enter type of algorithm,no of CPU's,no of IO's to start simulation...")
        print("Example : python main.py fcfs 2 1")
    else:
        no_of_cpus = sys.argv[2]
        no_of_ios = sys.argv[3]
        type = sys.argv[1]
        if type == 'rr':
            time_slice_check = int(sys.argv[4])
        filename = 'datafile.dat'
        process_list = getprocesses(filename)
        #print(sys.argv[1])
        create_pcbs(process_list)
        
        scheduler(len(process_list),type,int(no_of_cpus),int(no_of_ios),time_slice_check)
        
    # with open('fonts.txt') as f:
    #    p = f.readlines()
    # for item in p:
    #     f = Figlet(font = item)
    #     print(colored(f.renderText(' SIMULATION COMPLETE...!  '),"green"))
#     print('''||-----------------------------------------------------------------------||
# ||-----------------------------------------------------------------------||
# ||                   SIMULATION COMPLETE...!                             ||
# ||-----------------------------------------------------------------------||
# ||-----------------------------------------------------------------------||''')
    
    # with alive_bar(100, bar = 'blocks', spinner = 'notes2') as bar:
    #     for i in range(100):
    #         sleep(0.03)
    #         bar()                        # call after consuming one item
    # with alive_bar(100, bar = 'bubbles', spinner = 'notes2') as bar:
    #     for i in range(100):
    #         sleep(0.03)
    #         bar()                        # call after consuming one item










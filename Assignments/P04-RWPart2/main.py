from asyncio import threads
from dataclasses import dataclass
from sys import argv
import sys
import threading
import time
import copy
import json
from gen_inst import RandInstructions
from collections.abc import MutableMapping
from random import randint, shuffle
import random
from display_help import *
from helper_classes import *
from handleMemory import *
from Queue import *

threads=[]
pcb_list=[]
round_robin_quantum = 7
reg = Registers(4)


if __name__ == '__main__':
    if len(sys.argv[:])<3:
        print("Incorrect usage...")
        print("Please enter no of Writers,local/nonlocal for instruction preference...\n")
        print("Example : python main.py 5 l or nl \n")
    else:
        # CREATE SHARED MEMORY + A LOCAL COPY(DICTIONARY) OF THE SAME
        create_memory = handle_memory()

        #print(create_memory.localmemory())
        local_memory = create_memory.localmemory()

        with open("memory.json") as f:
            mem = json.load(f)
        with open( "mem_initial.json" ,"w") as f:
            json.dump(mem, f, indent=4)
        with open("mem_initial.json") as f:
            initial_data = json.load(f)
        # CREATE INSTRUCTION FILES BASED ON INPUT OF WRITERS
        no_of_writers = sys.argv[1]
        locking = sys.argv[2]

        all_instrs_of_writers = create_instr(int(no_of_writers)) # returns a dictionary

        # SORT THE INSRTUCTIONS FOR PRIVILIGED ONES
        if locking == 'l':
            all_instrs_of_writers = order_privileged_instr(all_instrs_of_writers)

        pcb_list = create_pcbs(int(no_of_writers),all_instrs_of_writers)
        no_of_totalinstr = findtotal(all_instrs_of_writers)

        locks_list=[]
        rw_lock = RWLock()
        locks_list.append(rw_lock)

        display = Helper_methods()
       
        layout = display.make_layout_mem()
        layout["header"].update(Header())
        layout["side"].update(Panel("Initial Memory - ", border_style="#00FF00"))
        layout["body"].update(Panel("Modified Memory - ", border_style="#00FF00"))
        layout["footer"].update(Panel(progress_table, border_style="#00FF00",title="[b]OVERALL PROGRESS[b]",))
        
        with Live(layout, screen=True, redirect_stderr=False) as live:
            try:
                for i in range(int(no_of_writers)):
                    threads.append(Writer(lock=locks_list,lock_pref = locking,instr=all_instrs_of_writers[i],init_sleep_time=((i+1)/10),memoryobject=create_memory,reg=reg,num=i+1,layout = layout,numofwriters=no_of_writers,noofinstr=no_of_totalinstr))

                for t in threads:
                    t.start()

                for t in threads:
                    t.join()
                with open("memory.json") as f:
                    modified_data = json.load(f)
                layout["side"].update(Panel("\n\n\n\n\n\n WRITING OF ALL PROCESSES COMPLETE,THE SNAPSHOTS NOW ARE ...", border_style="#00FF00"))
                layout["body"].update(Panel("\n\n\n\n\n\n WRITING OF ALL PROCESSES COMPLETE,THE SNAPSHOTS NOW ARE...", border_style="#00FF00"))
                time.sleep(0.1)
                layout["side"].update(Panel(display.loaddata_to_table(initial_data," BEFORE"), border_style="#00FF00"))
                layout["body"].update(Panel(display.loaddata_to_table2(initial_data,modified_data," AFTER COMPLETION OF WRITING"), border_style="#00FF00"))
                
                input("Enter") 
            except KeyboardInterrupt:
                pass

        # display = Helper_methods()
        # layout = display.make_layout()
        # layout["header"].update(Header())
        # layout["main"].update(Panel("Writers - ", border_style="#00FF00"))
        
        # with Live(layout, screen=True, redirect_stderr=False) as live:
            
        #     try:
        #         no_of_writers = sys.argv[1]
        #         no_of_readers = 5*int(no_of_writers)

        #         instr_pref = sys.argv[2] 
        #         locking = sys.argv[3]

        #         delays = [0,0.1,0.2]
        #         all_instr = create_instr(instr_pref,no_of_writers)
        #         reader_list = all_instr[int(no_of_writers):]

        #         threads = []

        #         reg = Registers(2)
        #         cpu = Cpu(reg)

        #         for i in range(int(no_of_writers)):
        #             shuffle(delays)
        #             threads.append(Writer(lock=locks_list,init_sleep_time=(1/10),sleep_time=delays[0],instr=all_instr[i],l=l,reg=reg,num=i+1,layout=layout))
        #             #threads.append(Writer(lock=locks_list,init_sleep_time=(i+1/10),sleep_time=delays[0],instr=all_instr[i],l=l,reg=reg,num=i+1,layout=layout))

        #         shuffle(threads)
        #         for t in threads:
        #             a = t.start()
        #             l = a
        #         for t in threads:
        #             t.join()
                
        #         with open("memory.json") as f:
        #             data = json.load(f)
        #         layout["main"].update(Panel("blah", border_style="#00FF00"))
        #         input("Enter") 
        #     except KeyboardInterrupt:
        #         pass

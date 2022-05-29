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

if __name__ == '__main__':
    if len(sys.argv[:])<4:
        print("Incorrect usage...")
        print("Please enter no of Writers,local/nonlocal,all/nec for instruction & lock preference...\n")
        print("Example : python main.py 5 local all\n")
    else:
    # CREATE SHARED MEMORY + A LOCAL COPY(DICTIONARY) OF THE SAME
        l = handle_memory()
        m = l.localmemory()
        with open("memory.json") as f:
            dataf = json.load(f)
        
        display = Helper_methods()
        layout = display.make_layout()
        layout["header"].update(Header())
        layout["side"].update(Panel("Writers - ", border_style="#00FF00"))
        layout["body"].update(Panel("Readers - ", border_style="#00FF00"))
        with Live(layout, screen=True, redirect_stderr=False) as live:
            try:
                no_of_writers = sys.argv[1]
                no_of_readers = 5*int(no_of_writers)

                instr_pref = sys.argv[2] 
                locking = sys.argv[3]

                delays = [0,0.1,0.2,0.3]
                all_instr = create_instr(instr_pref,no_of_writers)
                reader_list = all_instr[int(no_of_writers):]
                locks_list=[]
                if locking == 'all':
                    rw_lock = RWLock()
                    locks_list.append(rw_lock)
                elif locking == 'nec':
                    rw_lock_A = RWLock()
                    rw_lock_B = RWLock()
                    rw_lock_C = RWLock()
                    locks_list.append(rw_lock_A)
                    locks_list.append(rw_lock_B)
                    locks_list.append(rw_lock_C)
                threads = []

                reg = Registers(2)
                cpu = Cpu(reg)
                total_entry_time = time.time()
                for i in range(int(no_of_writers)):
                    shuffle(delays)
                    threads.append(Writer(lock=locks_list,init_sleep_time=(i/10),sleep_time=delays[0],instr=all_instr[i],l=l,reg=reg,num=i+1,layout=layout,no_of_writers=no_of_writers,locking=locking))
                    #threads.append(Writer(lock=locks_list,init_sleep_time=(i+1/10),sleep_time=delays[0],instr=all_instr[i],l=l,reg=reg,num=i+1,layout=layout))
                for i in range(int(no_of_readers)):
                    shuffle(delays)
                    # threads.append(Reader(rw_lock,(i/10),delays[0],reader_list[i],l,m,reg,cpu,i+1,layout))
                    threads.append(Reader(lock=locks_list,init_sleep_time=(i/10),sleep_time=delays[0],instr=reader_list[i],l=l,reg=reg,num=i+1,layout=layout))

                shuffle(threads)
                for t in threads:
                    a = t.start()
                    l = a
                for t in threads:
                    t.join()
                total_end_time = time.time() - total_entry_time
                layout["side"].update(Panel("Total completion time " + str(total_end_time), border_style="#00FF00"))
                time.sleep(4)
                with open("memory.json") as f:
                    data = json.load(f)
                layout["side"].update(Panel(display.loaddata_to_table(dataf," BEFORE"), border_style="#00FF00"))
                layout["body"].update(Panel(display.loaddata_to_table2(dataf,data," AFTER"), border_style="#00FF00"))
                input("Enter") 
            except KeyboardInterrupt:
                pass

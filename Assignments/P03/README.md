## P02 - CPU Scheduling
### Amulya Ejjina
### Description:
Cpu scheduling is a classic and contemporary computer science problem that started when early computers had processors that remained idle much of the time. The goal initially was to get multiple programs loaded into memory, so they could run back to back. This was still inefficient and needed improvement. That soon evolved into multiple programs loaded into memory and when one process blocked itself, the cpu would work on another available process (multi-programming).

This project mimics the CPU scheduling of processes by using a bunch of 
scheduling algorithms.

### Aim of the project:
To find out the efficiency of multiple algorithms by finding wait times - CPU WaitTime,IO Wait Time
and maximize throughput ,minimize wait times

### Detailed description of approach:
This project tries to simulate a real world CPU processing starting with
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


### Files

|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | sim.py         | Main driver of my project that launches simulation.      |
|   2   | Clock.py  | A singleton class which is used as a clock for simulation         |
|   3   | Cpu_singleton.py | A singleton CPU class to simulates a cpu resources |
|   4  | Io_singleton.py | A singleton IO class to simulates a cpu resources |
|   5   | table.py | A static table loaded with data of multiple runs,this is to just compare our statistics of multiple algorithms |
|   6   | Queue.py | A queue class made with list |
|   7  | Pcb.py | A process control block class which tracks everything related to a process starting from arrival times of the process to the termination time |
|   8   | gen_input.py | A class which creates input process list |
|   9  | display_helper.py | A class which has all methods which support display/visual of simulation using Rich library |
|   8   | gen_input.py | A class which creates input process list |

### Instructions

- Make sure you install library `Rich`
- My program expects two parameters to be placed on the command line when you run the program.
- Parameters `<number of cpus> <number of ios>`

- Example Command:
    - `python <sim.py> <number of cpus> <number of ios>`
    - `python sim.py 1 1`
    -  For round robin, `python sim.py 1 1 3`,3 being time slice/time quantum

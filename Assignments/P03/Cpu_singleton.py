
''' --------------------------------------------------------------------------
CLASS : Cpu_singleton
A CPU class to simulates a cpu resource
DESIGN PATTERN USED - SINGLETON
Methods :  
        - run_process()     : places a process on the cpu
        - remove_process()  : removes a process from the cpu
        - isbusy()          : checks if cpu is busysedn
-------------------------------------------------------------------------------
'''

class Cpu_singleton:
    __single = None
    def __init__(self,pcb = None):
        if not Cpu_singleton.__single:
            # Starting clock at 0
            self.running_process = pcb
        else:
            raise RuntimeError('A Singleton already exists') 

    @classmethod
    def getInstance(cls):
        if not cls.__single:
            cls.__single = Cpu_singleton()
        return cls.__single

    def run_process(self, pcb):
        if self.running_process is None:
            self.running_process = pcb
            return True
        else:
            raise Exception("CPU is busy...")
        return False

    def remove_process(self):
        if self.running_process is None:
            return ("No process is in cpu,cant remove any...")
        pcb = self.running_process
        self.running_process = None
        return {"process no= "+pcb.pid+" removed from cpu"}

    def isbusy(self):
        # return not len(self.running_process) < self.maxCpus
        return not self.running_process is None
    def cpuid(self):
        return 1


class Cpu_singleton2:
    __single = None
    def __init__(self,pcb = None):
        if not Cpu_singleton2.__single:
            # Starting clock at 0
            self.running_process = pcb
        else:
            raise RuntimeError('A Singleton already exists') 

    @classmethod
    def getInstance(cls):
        if not cls.__single:
            cls.__single = Cpu_singleton2()
        return cls.__single

    def run_process(self, pcb):
        if self.running_process is None:
            self.running_process = pcb
            return True
        else:
            raise Exception("CPU is busy...")
        return False

    def remove_process(self):
        if self.running_process is None:
            return ("No process is in cpu,cant remove any...")
        pcb = self.running_process
        self.running_process = None
        return {"process no= "+pcb.pid+" removed from cpu"}

    def isbusy(self):
        # return not len(self.running_process) < self.maxCpus
        return not self.running_process is None
    def cpuid(self):
        return 2

class Cpu_singleton3:
    __single = None
    def __init__(self,pcb = None):
        if not Cpu_singleton3.__single:
            # Starting clock at 0
            self.running_process = pcb
        else:
            raise RuntimeError('A Singleton already exists') 

    @classmethod
    def getInstance(cls):
        if not cls.__single:
            cls.__single = Cpu_singleton3()
        return cls.__single

    def run_process(self, pcb):
        if self.running_process is None:
            self.running_process = pcb
            return True
        else:
            raise Exception("CPU is busy...")
        return False

    def remove_process(self):
        if self.running_process is None:
            return ("No process is in cpu,cant remove any...")
        pcb = self.running_process
        self.running_process = None
        return {"process no= "+pcb.pid+" removed from cpu"}

    def isbusy(self):
        # return not len(self.running_process) < self.maxCpus
        return not self.running_process is None
    def cpuid(self):
        return 3

def singleton_check():
        print ("\nSINGLETON PATTERN CHECK\n")
        
        A = Cpu_singleton.getInstance()
        B = Cpu_singleton.getInstance()
        print(A is B)

        print ("At first B.clock= {} and A.clock = {}".format(B.running_process,A.running_process))
        #A.running_process = pcb_dict['0'][0]
        print ("After A.running process is assigned")
        print ("Now both B.x = {} and A.x = {} are same\n".format(B.running_process,A.running_process))
        print ( "Are A and B the same object? Answer: {}".format(id(A)==id(B)))
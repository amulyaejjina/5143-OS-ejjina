''' --------------------------------------------------------------------------
CLASS : Io_singleton
DESIGN PATTERN USED - SINGELTON
Methods :  
        - run_process()     : places a process on the io
        - remove_process()  : removes a process from the io
        - isbusy()          : checks if io is busy
------------------------------------------------------------------------------
'''
class Io_singleton:
    __single = None
    def __init__(self,pcb = None):
        if not Io_singleton.__single:
            self.running_process = pcb
        else:
            raise RuntimeError('A Singleton already exists') 

    @classmethod
    def getInstance(cls):
        if not cls.__single:
            cls.__single = Io_singleton()
        return cls.__single

    def run_process(self, pcb):
        if self.running_process is None:
            self.running_process = pcb
            return True
        else:
            raise Exception("IO is busy...")
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

    def ioid(self):
        return 1

class Io_singleton2:
    __single = None
    def __init__(self,pcb = None):
        if not Io_singleton2.__single:
            self.running_process = pcb
        else:
            raise RuntimeError('A Singleton already exists') 
    @classmethod
    def getInstance(cls):
        if not cls.__single:
            cls.__single = Io_singleton2()
        return cls.__single

    def run_process(self, pcb):
        if self.running_process is None:
            self.running_process = pcb
            return True
        else:
            raise Exception("IO is busy...")
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
    def ioid(self):
        return 2

class Io_singleton3:
    __single = None
    def __init__(self,pcb = None):
        if not Io_singleton3.__single:
            self.running_process = pcb
        else:
            raise RuntimeError('A Singleton already exists') 
    @classmethod
    def getInstance(cls):
        if not cls.__single:
            cls.__single = Io_singleton3()
        return cls.__single

    def run_process(self, pcb):
        if self.running_process is None:
            self.running_process = pcb
            return True
        else:
            raise Exception("IO is busy...")
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
    def ioid(self):
        return 3
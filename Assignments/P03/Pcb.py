''' --------------------------------------------------------------------------------------
CLASS : Pcb
A process control block class which tracks everything related to a process starting from
arrival times of the process to the termination time

The CPUWaitTimes and IOWaitTimes gets written to this block for each process
------------------------------------------------------------------------------------------
'''
class Pcb:
    def __init__(self,ln):
        ln = ln.split()
        self.arrivalTime = ln[0]
        self.pid = ln[1]
        self.priority = ln[2]
        self.burst = ln[3:]
        self.allburst = ln[3:]
        self.cpuBursts = []
        self.ioBursts=[]
        self.totCPUTime=0
        self.totIOTime=0
        self.CPUWaittime=0
        self.IOWaittime=0
        self.endTime=0
        self.sumofCpuBursts = 0
        self.sumofremCpuBursts = 0
        self.TAT=0
        for i in range(0,len(self.burst),2):
            self.cpuBursts.append(self.burst[i])
        for i in range(1,len(self.burst)-1,2):
            self.ioBursts.append(self.burst[i])
        for i in self.cpuBursts:
            self.totCPUTime = self.totCPUTime+int(i)
        for i in self.ioBursts:
            self.totIOTime = self.totIOTime+int(i)
        for i in self.cpuBursts:
            self.sumofCpuBursts=self.sumofCpuBursts + int(i)
        self.Turnaroundtime =0
        self.TotCPUTime =0
        self.TotIOTime=0

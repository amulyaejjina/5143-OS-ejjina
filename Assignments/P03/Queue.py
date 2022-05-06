''' --------------------------------------------------------------------------
CLASS : Queue - creating a queue structure with list
Methods :   
        - add()   - adds passed item to the Queue (append to list)
        - remove() - removes the first item from the Queue (pop from list)
        - length() - returns the length of the Queue
        - empty()  - returns if Queue is empty
        - first()  - gives the first element of the Queue (0th of the list)
        - last()   - gives the last element of the Queue (-1th of the list)
        - print()  - prints the Queue
        - removeall() - Removes all elements from the Queue
        - allitems()  - returns all items currently in the Queue
------------------------------------------------------------------------------
'''
class Queue:
    def __init__(self):
        self.Q = []

    def add(self,proc):
        self.Q.append(proc)

    def remove(self):
        return self.Q.pop(0)

    def remove_at(self,process):
        return self.Q.pop(self.Q.index(process))

    def remove_at_index(self,index):
        return self.Q.pop(index)
        
    def length(self):
        return len(self.Q)
                   
    def empty(self):
        return len(self.Q) == 0

    def first(self,key=None):
        if key is None:
            return self.Q[0]
        else:
            return self.Q[0][key]            

    def last(self,key=None):
        if key is None:
            return self.Q[-1]
        else:
            return self.Q[-1][key]   
    def print(self):
        print(self.Q)

    def removeall(self):
        self.Q.clear()
    def allitems(self):
        return self.Q

''' --------------------------------------------------------------------------
CLASS : clock
A Clock class to track the clock cycle for the simulation

DESIGN PATTERN USED - SINGLETON (only single instance of the class exists)
All instances created point to the same single instance of the class
------------------------------------------------------------------------------
'''
class Clock:
    __single = None 

    def __init__(self):
        if not Clock.__single:
            # Starting clock at 0
            self.clock = 0
        else:
            raise RuntimeError('A Singleton already exists') 

    @classmethod
    def getInstance(cls):
        if not cls.__single:
            cls.__single = Clock()
        return cls.__single


def singleton_check():
        print ("\nSINGLETON PATTERN CHECK\n")

        A = Clock.getInstance()
        B = Clock.getInstance()
        print(A is B)

        print ("At first B.clock= {} and A.clock = {}".format(B.clock,A.clock))
        A.clock = A.clock+1
        print ("After A.clock = 1")
        print ("Now both B.x = {} and A.x = {} are same\n".format(B.clock,A.clock))
        print ( "Are A and B the same object? Answer: {}".format(id(A)==id(B)))
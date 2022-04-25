from pprint import isreadable
from random import shuffle
import json
import random
from datetime import datetime


class RandInstructions:
    def __init__(self, **kwargs):
        """
        I want to generate instructions that are basically a single double or
        triple instruction.
        Where:
            1 = (2 reads, 1 op, 1 write)
            2 = (4 reads, 2 ops, 2 writes)
            3 = (6 reads, 3 ops, 3 writes)
        So I generate a list like [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3]
        which weighs more towards a single length instruction. When shuffled
        it looks like: [2, 3, 1, 1, 1, 3, 1, 2, 1, 1, 1, 2]. Now every time
        I generate an instruction, shuffle the list and choose the first value
        to determine instruction size.
        """
        # Build my list to determine instruction length
        shortInst = [1] * 7
        self.instLength = shortInst

        # get a seed from kwargs or use system time
        # this allows us to generate same output if necessary
        self.seed = kwargs.get("seed", datetime.now().timestamp())
        print(self.seed)
        random.seed(self.seed)

        # pull possible params from kwargs to tailor the building of
        # instructions
        self.addressRange = kwargs.get("addressRange", (100, 255, 5))
        self.choices = kwargs.get("choices", ["ADD", "SUB", "MUL", "DIV"])
        self.genAmount = kwargs.get("genAmount", 100)
        self.memblocks = kwargs.get("memblocks", ["A", "B", "C"])
        self.registers = kwargs.get("registers", ["R1", "R2"])
        self.retFormat = kwargs.get("retFormat", "json")  # or 'str'
        self.keepInstLocal = kwargs.get("keepInstLocal", False)
        self.isReader = kwargs.get("isReader", False)
        self.outFile = kwargs.get("outFile", "writer1.json")

        # build list to randomly choose memory addresses within proper range
        start, stop, step = self.addressRange
        self.memaddress = [x for x in range(start, stop, step)]

        # init vars that hold generated instructions
        self.strInstructions = ""
        self.listInstructions = []

        # shuffle all appropriate lists
        self.shuffleChoices()
        # generate the intructions
        self.generateInstructions()

    def shuffleChoices(self):
        """Shuffles all lists that need shuffling."""
        shuffle(self.instLength)
        shuffle(self.choices)
        shuffle(self.registers)
        shuffle(self.memblocks)
        shuffle(self.memaddress)

    def generateInstructions(self, num=None):
        """
        Params:
            num (int) : number of instructions to generate
        """
        # no num passed in, use default value in constructor
        if not num:
            num = self.genAmount

        # loop num times
        for _ in range(num):
            strInst = ""
            listInst = []
            # loop instruction length times for single,double, or triple length
            for _ in range(self.instLength[0]):
                self.shuffleChoices()

                itype = self.choices[0]
                r1, r2 = self.registers[:2]
                if self.keepInstLocal:
                        mb1 = mb2 = self.memblocks[0]
                else:
                        mb1, mb2 = self.memblocks[:2]

                madd1, madd2 = self.memaddress[:2]

                strInst += f"READ {mb1}{madd1} {r1}\n"
                strInst += f"READ {mb2}{madd2} {r2}\n"
                if not self.isReader:
                    strInst += f"{itype} {r1} {r2}\n"
                    strInst += f"WRITE {r1} {mb1}{madd1}\n"

                listInst.append(f"READ {mb1}{madd1} {r1}")
                listInst.append(f"READ {mb2}{madd2} {r2}")
                if not self.isReader:
                    listInst.append(f"{itype} {r1} {r2}")
                    listInst.append(f"WRITE {r1} {mb1}{madd1}")

            self.strInstructions += strInst
            self.listInstructions.append(listInst)

        if self.retFormat == "json":
            with open(self.outFile, "w") as f:
                json.dump(self.listInstructions, f, indent=3)
            return json.dumps(self.listInstructions, indent=3)

    def getJson(self):
        return json.dumps(self.listInstructions, indent=3)

    def getStr(self):
        return self.strInstructions
    def getList(self):
        return self.listInstructions


def randInstruction(asList = False):

    choices = ["ADD", "SUB", "MUL", "DIV"]
    registers = ["R1", "R2"]
    memblocks = ["A", "B", "C"]
    memaddress = [x for x in range(100, 255, 5)]

    shuffle(choices)
    shuffle(registers)
    shuffle(memblocks)
    shuffle(memaddress)

    itype = choices[0]
    r1, r2 = registers[:2]
    mb1, mb2 = memblocks[:2]
    madd1, madd2 = memaddress[:2]

    if not asList:
        inst = ""
        inst += f"READ {mb1}{madd1} {r1}\n"
        inst += f"READ {mb2}{madd2} {r2}\n"
        inst += f"{itype} {r1} {r2}\n"
        inst += f"WRITE {r1} {mb1}{madd1}\n"
    else:
        inst = []
        inst.append(f"READ {mb1}{madd1} {r1}")
        inst.append(f"READ {mb2}{madd2} {r2}")
        inst.append(f"{itype} {r1} {r2}")
        inst.append(f"WRITE {r1} {mb1}{madd1}")
    
    return inst
if __name__ == "__main__":
    # for i in range(10):
    #     print(randInstruction())
    if __name__ == "__main__":

        ri = RandInstructions(keepInstLocal=False)

        print(ri.getJson())
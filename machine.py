from typing import *

def trit_print(t : int):
    rep : str = ''
    for _ in range(11):
        rep += str(t % 3)
        t //= 3
    print(rep[::-1])

def str_to_trit(s : str) -> int:
    t = 0
    for _ in range(10):
        if s:
            t *= 3
            t += int(s[0]) 
            s = s[1:]
    return t

def crazy_op(a : int, memd : int) -> int:
    # do crazy_trit on each trit
    # TODO: check for off-by-one errors
    out = 0
    for place in range(10):  # machine words are 10 trits long
        out += crazy_trit(a % 3, memd % 3) * (3**place)
        a //= 3
        memd //= 3
    return out

def crazy_trit(a : int, d : int) -> int:
    if a == 0:
        return (d == 2) + 1
    elif a == 1:
        return (d == 2) * 2
    elif a == 2:
        return (3 - d) % 3
    else:
        raise Exception("That's not a trit!")

def rotate_right(memd : int) -> int:
    last_trit = memd % 3
    return (memd // 3) + last_trit*(3**9)

def scramble(i : int) -> int:
    if i not in range(33,127):
        raise Exception(f"Undefined behavior for scrambling chr({i})")
    refs : str = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    # this should never happen:
    if chr(i) not in refs:
        raise Exception("strings are weird...")
    outs : str = '5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK\'X~xDl}REokN:#?G"i@'
    return ord(outs[refs.index(chr(i))])

class InfernalMachine:
    """
    Malbolge virtual machine.
    Has some structs, probably, eventually.
    """

    # memory is based on trits.
    # Every machine word is 10 trits wide
    mem : List[int] = []
    # registers are one word wide, initially 0
    # C, the code register (@ inst to be executed) 
    C : int = 0
    # D, the data register (gpr)
    D : int = 0
    # A, the accumulator
    A : int = 0
    cyc : int = 0
    isStopped : bool = False
    isVerbose : bool = False
    

    def __init__(self):
        return

    def vprint(self, msg : Any):
        if self.isVerbose:
            print(msg)
        return

    def load_program(self, prog : str):
        # weird behavior if prog is too short, so just error.
        if len(prog) < 2:
            raise Exception("Program must be at least 2 characters long")
        # load program into memory as ints
        # whitespaces are skipped
        for c in prog:
            if not c.isspace():
                self.mem.append(ord(c))
        # every word in memory AFTER the program gets crazified
        fst = len(self.mem)
        # memory space is exactly 59049 words long
        for _ in range(fst, 3**10 + 1):
            self.mem.append(crazy_op(self.mem[-1], self.mem[-2]))
        #self.vprint(f'{self.mem}')
        return
    
    def run(self):
        while not self.isStopped:
            # execute the next instruction
            self.exec_next()
            # if [C] is in [33,126], encipher it
            # (otherwise, this is undefined behavior!)
            self.mem[self.C] = scramble(self.mem[self.C])
            self.vprint(f"Now [{self.C}] is {self.mem[self.C]}")
            # finally, increment C and D mod 3**10
            self.C = (self.C + 1) % (3**10)
            self.D = (self.D + 1) % (3**10)
            self.vprint(f"C: {self.C}\t\tD: {self.D}")
        
    def exec_next(self):
        pointed_code : int = self.mem[self.C]
        self.vprint(f"Inst to execute: {pointed_code} @ PC {self.C}")
        if pointed_code not in range(33,127):
            raise Exception(f"Invalid instruction {self.mem[self.C]}")
        inst = (pointed_code + self.C) % 94
        # TODO: update to python 3.9 and use a switch
        if inst == 4:
            # C = [D]
            self.vprint('i')
            self.C = self.mem[self.D]
        elif inst == 5:
            # PRINT(A%256)
            self.vprint('<')
            print(chr(self.A % 256), end='')
        elif inst == 23:
            # A = INPUT
            self.vprint('/')
            self.A = int(ord(input('> ')[0]))
        elif inst == 39:
            # A = [D] = ROTATE_RIGHT([D])
            self.vprint('*')
            rotated = rotate_right(self.mem[self.D])
            self.A = rotated
            self.mem[self.D] = rotated
        elif inst == 40:
            # D = [D]
            self.vprint('j')
            self.vprint(f"Setting D to {self.mem[self.D]}")
            self.D = self.mem[self.D]
        elif inst == 62:
            # A = [D] = CRAZY_OP(A, [D])
            self.vprint('p')
            crazified = crazy_op(self.A, self.mem[self.D])
            self.A = crazified
            self.mem[self.D] = crazified
        elif inst == 68:
            self.vprint('o')
            # NOP (these are the only explicit NOPs allowed)
        elif inst == 81:
            # STOP
            self.vprint('v')
            self.isStopped = True
        # otherwise do a nop.
        else:
            self.vprint('o')
        self.cyc += 1
        return
    
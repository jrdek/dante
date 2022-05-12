#!/usr/bin/pypy3
import machine
import sys

if __name__ == '__main__':
    if (len(sys.argv) < 2) or ((len(sys.argv) == 2) and (sys.argv[1] == '-v')):
        raise Exception("Usage: ./main.py FILE [-v]")    
    mach = machine.InfernalMachine()
    mach.isVerbose = ('-v' in sys.argv)
    with open(sys.argv[1]) as malfile:
        prog = '\n'.join(malfile.readlines())
    mach.load_program(prog)
    mach.run()
    print()

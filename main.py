from Interpreter import *
import sys

if len(sys.argv) > 1:
    if sys.argv[1] == "-version":
        print(f"VERSION: {Interpreter.version}")
    else:
        f = open(sys.argv[1])
        c = f.read()
        f.close()
        compile = False
        load_mode = False
        debug = False
        if len(sys.argv) > 2:
            if sys.argv[2] == "-compile":
                compile = True
            if sys.argv[2] == "-load":
                load_mode = sys.argv[1]
            if sys.argv[2] == "-debug":
                debug = True

        Interpreter(c, compile, load_mode, debug)
else:
    print("file as arg")
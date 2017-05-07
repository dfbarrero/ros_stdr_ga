#!/usr/bin/env python

from subprocess import call

arg = "".join(str(range(18))).replace(" ", "")
res = call(["rosservice", "call", "/computeFitness", arg])
print(res)


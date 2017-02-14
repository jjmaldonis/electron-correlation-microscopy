import os
import re

pattern = "\((?P<x>\d+),(?P<y>\d+)\)"
pattern = re.compile(pattern)

#test = "(130,129).data"
#print(
#pattern.search(test).groups()
#)

data = os.listdir("individual_spatial_data/")
pngs = os.listdir("individual_spatial_pngs/")

data = set(pattern.search(f).groups() for f in data)
pngs = set(pattern.search(f).groups() for f in pngs)

inputs = []
for f in ["inputs1.in", "inputs2.in", "inputs3.in", "inputs4.in"]:
    inputs.extend(open(f).readlines())
inputs = set(tuple(line.strip().split()) for line in inputs)

no_data = inputs - data
no_pngs = inputs - pngs
no_either = no_data | no_pngs

print(len(no_data))
print(len(no_pngs))
print(len(no_either))

with open("inputs_data.in", "w") as f:
    for x, y in no_data:
        f.write("{} {}\n".format(x,y))

with open("inputs_pngs.in", "w") as f:
    for x, y in no_pngs:
        f.write("{} {}\n".format(x,y))

with open("inputs_either.in", "w") as f:
    for x, y in no_either:
        f.write("{} {}\n".format(x,y))

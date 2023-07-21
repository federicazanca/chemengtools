import os
import sys
def text(m, n, file):
    lines = []
    i = 0
    for line in file:
        i = i+1
        if m < i < n:
            lines.append(line)
    return lines

if len(sys.argv) < 4:
    print("ERROR: not enough arguments.  Usage: python create_file.py file.cif template.cif chargedata")
    exit()



input = open(sys.argv[1])
example = open(sys.argv[2])
charges = open(sys.argv[3])

inizio = text(0, 11,example)
header = inizio[3].split()
header[1] ="'" +sys.argv[1] + "'\n"
inizio[3] = " ".join(header)
cell = text(10,17,input)


example.close()
example = open(sys.argv[2])
loop = text(17,25,example)

input.close()
input = open(sys.argv[1])
coords =[]
for line in input:
    tokens = line.split()
    if len(tokens) == 8:
        del tokens[6]
        del tokens[5]
        del tokens[1]
        coords.append(tokens)


i = 0
for line in charges:
    tokens =line.split()
    if len(tokens) == 0:
        continue
    if tokens[0] == "Charge":
        coords[i].append(tokens[-1])
        i = i+1

output = open("output.cif", "w")
for line in inizio:
    output.write(line)
for line in cell:
    output.write(line)
output.write("\n")
for line in loop:
    output.write(line)
for line in coords:
    output.write("   ".join(line))
    output.write("\n")

output.close()

#to check charge
output = open("output.cif", "r")
charge = 0
for line in output:
    if len(line.split()) == 6:
        charge = charge + float(line.split()[5])
        print(charge)
print(charge)
output.close()

import os
import time

os.system('qm list > AVMS.txt')
time.sleep(2)
os.system('sed -i \'1d\' AVMS.txt')
os.system('cut -c 8-10 AVMS.txt > newAVMS.txt && rm -rf AVMS.txt')
out = []

with open("newAVMS.txt") as fp:
    for i, line in enumerate(fp):
        out.append(line[:-1])
#print out
out2 = []
for i in range(400,500):
    out2.append(str(i))
#print out2
final = list(set(out2) - set(out))
final.sort()

print final
os.system('rm -rf newAVMS.txt')

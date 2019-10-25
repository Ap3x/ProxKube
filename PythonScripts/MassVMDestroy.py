import os 

cmdDelete = "qm destroy "
VMID =  600
End_VMID =  604

while VMID <= End_VMID:
    os.system(cmdDelete + str(VMID))
    VMID += 1

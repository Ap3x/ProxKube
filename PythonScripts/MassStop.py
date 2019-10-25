import os 

cmdDelete = "qm stop "
VMID =  401
End_VMID =  459

while VMID <= End_VMID:
    os.system(cmdDelete + str(VMID))
    VMID += 1

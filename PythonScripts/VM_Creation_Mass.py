import os

VMID_start = 425 #This is the VM ID start number
NumVMs = 34 #This is the number of VMs to create

for x in range(NumVMs):
    CreateCommand = "qm create "+str(VMID_start)+ " --name=VulnHub-"+str(VMID_start)+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --scsi0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
    os.system(CreateCommand)
    print "Created VM " + str(VMID_start)
    VMID_start += 1
print "Done: Created "+str(NumVMs)+" VMs"


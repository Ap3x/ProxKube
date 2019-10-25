import os
import sys
import re

VMID_Start = 461  #This is the VM ID start number
LoopNum = 1
state = 0 
textFileCreate =  "ls *.vmdk | sed  -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' > ConvertRAWfile.txt"
#textFileCreate =  "ls *.qcow2 | sed  -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' | tee ConvertRAWfile.txt"
os.system(textFileCreate)
with open("ConvertRAWfile.txt") as fp:
    for i, line in enumerate(fp):
	state = 0
        if state == 0:
	    try:
                print "Current File: "+ line[:-1]
                expr = re.compile(r".*<rasd:Description>(.+?)</rasd:Description>");
                out = []
                with open(line[:-1]+".ovf") as fp2:
                    for j, line2 in enumerate(fp2):
                        if expr.findall(line2) != []:
                            temp = expr.findall(line2)
                            out.append(temp[0])
                print " => " + str(out)

                elementNum = 0
                for data in out:
                    s = out[elementNum]

                    expr2 = re.compile(r'.*SATA');
                    new = expr2.findall(s)
                    if new:
                        print "FOUND SATA"
	    	        CreateCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --sata0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
	    	        break
                    expr3 = re.compile(r'.*IDE');
                    new3 = expr3.findall(s)
                    if new3:
                        print "FOUND IDE"
	    	        CreateCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --ide0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
	    	        break
                    expr4 = re.compile(r'.*SCSI');
                    new4 = expr4.findall(s)
                    if new4:
                        print "FOUND SCSI"
	    	        CreateCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --scsi0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
	    	        break
                    elementNum += 1
	    except IOError as e:
	        print "OVF File not found looking for VMX File"
	        state = 1
	if state == 1:
	    try:
                expr5 = re.compile(r".*ide0:0.present");
                out = []
                with open(line[:-1]+".vmx") as fp:
                    for k, line3 in enumerate(fp):
                        if expr5.findall(line3) != []:
                            temp = expr5.findall(line3)
                            out.append(temp[0])
			    CreateCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --ide0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
		expr6 = re.compile(r".*sata0:0.present");
                out = []
                with open(line[:-1]+".vmx") as fp:
                    for k, line4 in enumerate(fp):
                        if expr6.findall(line4) != []:
                            temp = expr6.findall(line4)
                            out.append(temp[0])
                            CreateCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --sata0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
                expr7 = re.compile(r".*scsi0:0.present");
                out = []
                with open(line[:-1]+".vmx") as fp:
                    for k, line5 in enumerate(fp):
                        if expr7.findall(line5) != []:
                            temp = expr7.findall(line5)
                            out.append(temp[0])
                            CreateCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --scsi0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
#		print " => " + str(out)
            except IOError as e:
                print "MISSING VMX or OVF file"
                sys.exit()

#       CreateCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --sata0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
#	CreateCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --ide0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
        os.system(CreateCommand)
        print "Created VM " + str(VMID_Start) +" called VulnHub-"+line[:-1]
        VMID_Start += 1
	LoopNum += 1
print "Done: Created "+str(LoopNum-1)+" VMs"


VMID_Start -= LoopNum
VMID_Start += 1

with open("ConvertRAWfile.txt") as fp:
    for i, line in enumerate(fp):
       cmdConvert = "qemu-img convert -f vmdk " +line[:-1]+ ".vmdk -O qcow2 " +line[:-1]+ ".qcow2"
       os.system(cmdConvert)
       print "Successful conversion of " + line[:-1]+ ".vmdk to " + line[:-1]+ ".qcow2"
       cmdMove = "mv " +line[:-1]+ ".qcow2 /Backup/images/"+str(VMID_Start)+"/vm-"+str(VMID_Start)+"-disk-1.qcow2"
       os.system(cmdMove)
       print "Moved "+line[:-1]+ ".qcow2 to  /Backup/images/"+str(VMID_Start)+"/vm-"+str(VMID_Start)+"-disk-1.qcow2"
#       os.system("rm -rf "+ line[:-1]+ ".raw")
#       print "Deleted "+ line[:-1]+ ".raw"
       VMID_Start += 1 
       print "Completed"

print "Converted and moved all the files"
os.system("rm -rf ConvertRAWfile.txt")

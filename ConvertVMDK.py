import os
import sys 
import re as regexLib

def mainMenu ():
    mmSelect = True
    while mmSelect:
        os.system('clear')
        print("   ___                                                     ___                          _            ")
        print("  / _ \_ __ _____  ___ __ ___   _____  __ /\   /\/\/\     / __\___  _ ____   _____ _ __| |_ ___ _ __ ")
        print(" / /_)/ '__/ _ \ \/ / '_ ` _ \ / _ \ \/ / \ \ / /    \   / /  / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__|")
        print("/ ___/| | | (_) >  <| | | | | | (_) >  <   \ V / /\/\ \ / /__| (_) | | | \ V /  __/ |  | ||  __/ |   ")
        print("\/    |_|  \___/_/\_\_| |_| |_|\___/_/\_\   \_/\/    \/ \____/\___/|_| |_|\_/ \___|_|   \__\___|_|   ")
        print("v1.0 http://github.com/Ap3x")
        print("\n")
        print("1-Convert VMDK")
        print("2-Convert QCOW2")
        print("3-Destroy VM(s)")
        print("4-Stop VM(s)")
        print("5-Start VM(s)")
        print("x-Exit")

        select = raw_input("Select an option: ")

        if select == "1":
            ConvertVMDK()
            ParseConf()

        elif select == "2":
            ConvertQCOW2()
            ParseConf()
        #elif select == "3":
        #
        #elif select == "4":
        #
        #elif select == "5":

def GetListOfVM():
	os.system('qm list > AVMS.txt')
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

	#print final
	os.system('rm -rf newAVMS.txt')


def ConvertVMDK ():
    path = raw_input("Path of folder with VMDK file(s): ")
    os.system("cd " + path)
    getFileName = "ls *.vmdk | sed  -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' > ConvertRAWfile.txt"	#List the files then removes the last 5 chars then puts each line in ConvertRAWfile
    os.system(getFileName)
    try:
        with open("ConvertRAWfile.txt") as fp:
            for i, line in enumerate(fp):
                SearchForOVF(line)
                SearchForVMX(line)
    except IOError as e:
        print("MISSING VMX or OVF file")
        sys.exit()


def ConvertQCOW2 ():
    path = raw_input("Path of folder with QCOW2 file(s): ")
    os.system("cd " + path)
    getFileName = "ls *.qcow2 | sed  -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' | tee ConvertRAWfile.txt" #List the files then removes the last 6 chars then puts each line in
                                                                                                                                       #ConvertRAWfile
    os.system(getFileName)
    try:
        with open("ConvertRAWfile.txt") as fp:
            for i, line in enumerate(fp):
                SearchForOVF(line)
                SearchForVMX(line)
    except IOError as e:
        print("MISSING VMX or OVF file")
        sys.exit()

def SearchForOVF (fileName):
    try:
        print("Current File: " + fileName)				            					# Read the first line of ConvertRAWfile.txt
        expression = regexLib.compile(r".*<rasd:Description>(.+?)</rasd:Description>")	# Expression to search for
        out = []
        with open(fileName + ".ovf") as enumFile:						            		# Search each line of the .ovf file IF the file is not
                                                 						            		# found then the error is caught and searches a vmx file
            for lineNum, lineInfo in enumerate(enumFile):					            # For each line in ovf file
                if expression.findall(lineInfo) != []:							        # Read the line looking for the expression
                    temp = expression.findall(lineInfo)							        # If found between Description tags in ovf add to temp
                    out.append(temp[0])										            # temp is added to array
        print(" => " + str(out))
    except IOError as e:
       print("OVF File not found looking for VMX File")

def SearchForVMX (fileName):
        expr = regexLib.compile(r".*ide0:0.present")
        out = []
        with open(fileName + ".vmx") as enumFile:
            for lineNum, lineInfo in enumerate(enumFile):
                if expr.findall(lineInfo) != []:
                    temp = expr.findall(lineInfo)
                    out.append(temp[0])
                    CreateVMfromVMX("ide")

        expr = re.compile(r".*sata0:0.present")
        out = []
        with open(fileName + ".vmx") as enumFile:
            for lineNum, lineInfo in enumerate(enumFile):
                if expr.findall(lineInfo) != []:
                    temp = expr.findall(lineInfo)
                    out.append(temp[0])
                    CreateVMfromVMXby("sata")

        expr = regexLib.compile(r".*scsi0:0.present")
        out = []
        with open(fileName + ".vmx") as enumFile:
            for lineNum, lineInfo in enumerate(enumFile):
                if expr.findall(lineInfo) != []:
                    temp = expr.findall(lineInfo)
                    out.append(temp[0])
                    CreateVMfromVMX("scsi")

def CreateVMfromVMXbyIDE (vmID, vmName, typeOfHD):
    createCommand = "qm create " + str(vmID) + " --name=" + vmName + " --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --" + typeOfHD + "0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
    return createCommand

def CreateVMfromOVF (vmID, vmName, typeOfHD):
    createCommand = "qm create " + str(vmID) + " --name=" + vmName + " --onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --" + typeOfHD + "0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"

def CreateVM (command, vmID, vmName):
    os.system(command)
    print("Created VM " + str(vmId) + " called " + vmName)

def ParseOVF ():
    VMID_Start = 461  #This is the VM ID start number
    LoopNum = 1
    with open("ConvertRAWfile.txt") as enumFile:
        for i, line in enumerate(enumFile):
            if state == 0:
                try: 
                    SearchOVF()
                    elementNum = 0
                    for data in out:
                        s = out[elementNum]
                        expr2 = regexLib.compile(r'.*SATA')
                        expr3 = regexLib.compile(r'.*IDE')
                        expr4 = regexLib.compile(r'.*SCSI')

                        new = expr2.findall(s)
                        if new:
                            CreateVMfromOVF("sata")
                            break

                        new3 = expr3.findall(s)
                        if new3:
                            CreateVMfromOVF("ide")
                            break

                        new4 = expr4.findall(s)
                        if new4:
                            CreateVMfromOVF("scsi")
                            break
                        elementNum += 1
                except IOError as e:
                    print("OVF File not found looking for VMX File")
#   createCommand = "qm create "+str(VMID_Start)+ "
#   --name=VulnHub-"+line[:-1]+" --onboot=1 --ide2=none,media=cdrom
#   --ostype=l26 --scsihw=virtio-scsi-pci --sata0=Backup:1,format=qcow2
#   --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1"
#	createCommand = "qm create "+str(VMID_Start)+ " --name=VulnHub-"+line[:-1]+"
#	--onboot=1 --ide2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci
#	--ide0=Backup:1,format=qcow2 --sockets=1 --cores=1 --numa=0 --memory=512
#	--net0=virtio,bridge=vmbr1"
#CreateVM()
#print("Created VM " + str(VMID_Start) +" called VulnHub-"+line[:-1])
#VMID_Start += 1
#LoopNum += 1
#print("Done: Created "+str(LoopNum-1)+" VMs")
#
#VMID_Start -= LoopNum
#VMID_Start += 1

#####with open("ConvertRAWfile.txt") as enumFile:
#####    for i, line in enumerate(enumFile):
#####       cmdConvert = "qemu-img convert -f vmdk " + line[:-1] + ".vmdk -O qcow2 " + line[:-1] + ".qcow2"
#####       os.system(cmdConvert)
#####       print("Successful conversion of " + line[:-1] + ".vmdk to " + line[:-1] + ".qcow2")
#####       cmdMove = ("mv " + line[:-1] + ".qcow2 /Backup/images/" + str(VMID_Start) + "/vm-" + str(VMID_Start) + "-disk-1.qcow2")
#####       os.system(cmdMove)
#####       print("Moved " + line[:-1] + ".qcow2 to  /Backup/images/" + str(VMID_Start) + "/vm-" + str(VMID_Start) + "-disk-1.qcow2")
######       os.system("rm -rf "+ line[:-1]+ ".raw")
######       print "Deleted "+ line[:-1]+ ".raw"
#####       VMID_Start += 1 
#####       print("Completed")
#####
#####print("Converted and moved all the files")
#####os.system("rm -rf ConvertRAWfile.txt")

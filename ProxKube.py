#!/usr/bin/python
import os
import sys 
import re as regexLib

# TODO
# Get list of open vmID numbers
# Setup options for VM (sockets, cores, memory)
# Menu option to download and unzip the ova, gz, 7z
# Start VM after created

#This is the mounted directory location for your image files (e.g. /var/lib/vz)
dirLocation="/var/lib/vz/" #CHANGE THIS
storageName="NetworkShare"   #CHANGE THIS
tempFile="/tmp/ConvertRAWfile.txt"
tempVMFile="/tmp/AVMS.txt"

def download_vuln():
    link = raw_input("What is the download link? ")
    os.system("echo " + link + "| cut -d / -f 5 | sed 's/.\{4\}$//'" )
    os.system("wget "+ link + " && tar -xvf " + link)

def print_banner():
    os.system('clear')
    print(" ________  ________  ________     ___    ___ ___  __    ___  ___  ________  _______       ")
    print("|\   __  \|\   __  \|\   __  \   |\  \  /  /|\  \|\  \ |\  \|\  \|\   __  \|\  ___ \      ")
    print("\ \  \|\  \ \  \|\  \ \  \|\  \  \ \  \/  / | \  \/  /|\ \  \\\  \ \  \|\ /\ \   __/|     ")
    print(" \ \   ____\ \   _  _\ \  \\\  \  \ \    / / \ \   ___  \ \  \\\  \ \   __  \ \  \_|/__   ")
    print("  \ \  \___|\ \  \\  \\ \  \\\  \  /     \/   \ \  \\ \  \ \  \\\  \ \  \|\  \ \  \_|\ \  ")
    print("   \ \__\    \ \__\\ _\\ \_______\/  /\   \    \ \__\\ \__\ \_______\ \_______\ \_______\ ")
    print("    \|__|     \|__|\|__|\|_______/__/ /\ __\    \|__| \|__|\|_______|\|_______|\|_______| ")
    print("                                 |__|/ \|__|                                              ")
    print("v1.1 http://github.com/Ap3x\n")

def print_menu():
    print("1-Convert All VMDK")
    print("2-Download VulnHub Mirror Link (.ova)")
    print("3-Destroy VM(s)")
    print("4-Stop VM(s)")
    print("5-Start VM(s)")
    print("x-Exit")
    return raw_input("Select an option: ")

def convert_vmdk():
    os.system("cd " + raw_input("Path of folder with VMDK file(s): "))
    os.system("ls *.mf | sed 's/.\{3\}$//' > " + tempFile)
    print("1) LVM-Thin")
    print("2) Directory ")
    storageChoice = int(raw_input("What kind of storage are you using: "))
    
    try:
        with open(tempFile) as fp:
            for i, line in enumerate(fp):
                # The line below will be replaced with getting the starting VM ID and just filling in where there isnt VMIDs
                vmIdInput = int(raw_input("What is the VM ID: "))
                fileFound = find_config(line[:-1])
                if fileFound:
                    parse_config(vmIdInput, line[:-1],".vmx", storageChoice)
                elif not fileFound:
                    parse_config(vmIdInput, line[:-1],".ovf", storageChoice)
                    

                else:
                    raise Exception()
    except IOError as e:
        print("MISSING VMX or OVF file" + str(e) )
        os.system("rm -rf " + tempFile)
        sys.exit()
        # elif(storageChoice == 1):
        #     with open(tempFile) as fp:
        #         for i, line in enumerate(fp):
        #             vmIdInput = int(raw_input("What is the VM ID: "))
        #             convert_vmdk_raw(vmIdInput)

def find_config(fileName):
    try:
        print("Current File: " + fileName)				            					# Read the first line of ConvertRAWfile.txt
        expression = regexLib.compile(r".*<rasd:Description>(.+?)</rasd:Description>")	# Expression to search for
        os.system("ls " + fileName + "*.ovf | sed 's/.\{3\}$//' > /tmp/findconfig.txt" )
        with open("/tmp/findconfig.txt") as enumFile:						            	# Search each line of the .ovf file IF the file is not                          						            		# found then the error is caught and searches a vmx file
            for lineNum, lineInfo in enumerate(enumFile):					            # For each line in ovf file
                if expression.findall(lineInfo) != []:							        # Read the line looking for the expression
                    temp = expression.findall(lineInfo)							        # If found between Description tags in ovf add to temp
                    out.append(temp[0])										            # temp is added to array
                    print(" => " + str(out))
                    return  True
    except IOError as e:
        print("OVF File not found looking for VMX File " + str(e) )

def parse_config(vmId,fileName,fileType, storageType):
	
    if(fileType == ".vmx"):
        os.system("ls " + fileName + "*.vmx | sed 's/.\{3\}$//' > /tmp/findconfig2.txt" )
        expr = regexLib.compile(r".*ide0:0.present")
        expr1 = regexLib.compile(r".*sata0:0.present")
        expr2 = regexLib.compile(r".*scsi0:0.present")
        out = []
        with open(fileName + fileType) as enumFile:
            for lineNum, lineInfo in enumerate(enumFile):
                if expr.findall(lineInfo) != [] :
                    temp = expr.findall(lineInfo)
                    out.append(temp[0])
                    build_vm_command(vmId,fileName,"ide", "vmx", storageType)
                elif expr1.findall(lineInfo) != []:
                    temp = expr1.findall(lineInfo)
                    out.append(temp[0])
                    build_vm_command(vmId,fileName,"sata", "vmx", storageType)
                elif expr2.findall(lineInfo) != []:
                    temp = expr2.findall(lineInfo)
                    out.append(temp[0])
                    build_vm_command(vmId,fileName,"scsi", "vmx", storageType)

    elif(fileType == ".ovf"):
        expr2 = regexLib.compile(r'.*SATA')
        expr3 = regexLib.compile(r'.*IDE')
        expr4 = regexLib.compile(r'.*SCSI')
        os.system("ls " + fileName + "*.ovf | sed 's/.\{4\}$//' > /tmp/findconfig2.txt" )
        with open(fileName + fileType) as enumFile:
            for lineNum, lineInfo in enumerate(enumFile):
                try:
                    if expr2.findall(lineInfo):
                        build_vm_command(vmId, fileName, "sata", "ovf", storageType)
                        break
                    elif expr3.findall(lineInfo):
                        build_vm_command(vmId, fileName, "ide", "ovf", storageType)
                        break
                    elif expr4.findall(lineInfo):
                        build_vm_command(vmId, fileName, "scsi", "ovf", storageType)
                        break
                except IOError as e:
                    os.system("rm -rf " + tempFile)
                    print("OVF File not found looking for OVF File")

def build_vm_command(vmId, vmName, typeOfHD, fileType, storageType):
    if(storageType == 1):
        createCommand = "qm create " + str(vmId) + " --name=" + vmName + " --onboot=0 --"+ typeOfHD +"2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --" + typeOfHD + "0=" + storageName + ":1,format=raw,cache=writethrough --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1,tag=700"
    elif(storageType == 2 ):
        createCommand = "qm create " + str(vmId) + " --name=" + vmName + " --onboot=0 --"+typeOfHD+"2=none,media=cdrom --ostype=l26 --scsihw=virtio-scsi-pci --" + typeOfHD + "0=" + storageName + ":1,format=qcow2,cache=writethrough --sockets=1 --cores=1 --numa=0 --memory=512 --net0=virtio,bridge=vmbr1,tag=700"
   
    create_vm(createCommand, vmId, vmName)
   
    if(storageType == 1):
        convert_vmdk_raw(vmId, vmName) 
    elif(storageType == 2):
        convert_vmdk_qcow2(vmId, vmName)

def create_vm(command, vmId, vmName):
    os.system(command)
    print("Created VM " + str(vmId) + " called " + vmName)

def convert_vmdk_qcow2(vmId, vmName):
    os.system("ls " + vmName + "*.ovf | sed 's/.\{4\}$//' > /tmp/findconfig.txt" )

    with open("/tmp/findconfig.txt") as enumFile:						            	# Search each line of the .ovf file IF the file is not                          						            		# found then the error is caught and searches a vmx file
        for lineNum, lineInfo in enumerate(enumFile):
            os.system("qemu-img convert -f vmdk " + lineInfo + ".vmdk -O qcow2 " + lineInfo + ".qcow2")
            print("Successful conversion of " + lineInfo + ".vmdk to " + lineInfo + ".qcow2")
    
            os.system("mv " + lineInfo + ".qcow2 "+ dirLocation +"images/" + str(vmId) + "/vm-" + str(vmId) + "-disk-0.qcow2")
            print("Moved " + lineInfo + ".qcow2 to  "+ dirLocation +"images/" + str(vmId) + "/vm-" + str(vmId) + "-disk-1.qcow2")
            print("Completed")

def convert_vmdk_raw(vmId, vmName):
    os.system("ls " + vmName + "*.vmdk | sed 's/.\{5\}$//' > /tmp/findconfig.txt" )

    with open("/tmp/findconfig.txt") as enumFile:						            	
        for lineNum, lineInfo in enumerate(enumFile):
            #qemu-img convert -O raw /data/source.vmdk /data/output.raw
            os.system("qemu-img convert -O raw " + lineInfo[:-1] + ".vmdk " + vmName + ".raw")
            print "Currently replacing " + lineInfo[:-1]+ ".raw for /dev/" + storageName + "/vm-" + str(vmId)+ "-disk-0"
            os.system("mv " + vmName + ".raw /dev/" + storageName + "/vm-" +str(vmId)+ "-disk-0")
            print "Successfully copied " + vmName + ".raw for /dev/" + storageName + "/vm-" + str(vmId)+ "-disk-0"
            #cmdConvert = "mv " +lineInfo[:-1]+ ".vmdk /Data-ISO2/template/iso/."
            #print "Moved %s.vmdk" % lineInfo[:-1]
            print "Completed"

#In Development:
def get_vm_list():
	os.system('qm list > ' + tempVMFile)
	os.system('sed -i \'1d\' ' + tempVMFile)
	os.system('cut -c 8-10 ' + tempVMFile + ' > ' + tempVMFile)
	out = []
	with open(tempVMFile) as fp:
		for i, line in enumerate(fp):
			out.append(line[:-1])
	out2 = []
	for i in range(400,500):
		out2.append(str(i))
	final = list(set(out2) - set(out))
	final.sort()

	#print final
	os.system('rm -rf ' + tempVMFile)
	os.system('rm -rf /tmp/findconfig.txt')

print_banner()
option = print_menu()
if option == "1":
    convert_vmdk()
elif option == "2":
    download_vuln()
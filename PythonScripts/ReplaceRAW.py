import os

textFileCreate =  "ls *.raw | sed  -e 's/.$//' -e 's/.$//' -e 's/.$//' -e 's/.$//' | tee ConvertRAWfile.txt"
os.system(textFileCreate)

vmStartNum = 422

with open("ConvertRAWfile.txt") as fp:
    for i, line in enumerate(fp):
       print "Currently replacing " + line[:-1]+ ".raw for /dev/Data-Disk/vm-" + str(vmStartNum)+ "-disk-1"
       cmdReplace = "mv " +line[:-1]+ ".raw /dev/Data-Disk/vm-" +str(vmStartNum)+ "-disk-1"
       os.system(cmdReplace)
       print "Successfully copied " + line[:-1]+ ".raw for /dev/Data-Disk/vm-" + str(vmStartNum)+ "-disk-1"
       #cmdConvert = "mv " +line[:-1]+ ".vmdk /Data-ISO2/template/iso/."
       #print "Moved %s.vmdk" % line[:-1]
       vmStartNum += 1
       print "Completed"
print "Replaced all the files"
os.system("rm -rf ConvertRAWfile.txt")


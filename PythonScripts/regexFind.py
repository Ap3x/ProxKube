import re
import sys
fileName = "2.0_ptr_1" #WITHOUT file format (e.g. .vmx , .ovf)

try:
    expr = re.compile(r".*<rasd:Description>(.+?)</rasd:Description>");
    out = []
    with open(fileName+".ovf") as fp:
        for i, line in enumerate(fp):
    	    if expr.findall(line) != []:
    	    	temp = expr.findall(line)
    	    	out.append(temp[0])
    print " => " + str(out)
    
    elementNum = 0
    for data in out:
        s = out[elementNum]
    #    print s
        expr2 = re.compile(r'.*SATA');
        new = expr2.findall(s)
        if new:
            print "FOUND SATA"
        expr3 = re.compile(r'.*IDE');
        new3 = expr3.findall(s)
        if new3:
            print "FOUND IDE"
        expr4 = re.compile(r'.*SCSI');
        new4 = expr4.findall(s)
        if new4:
            print "FOUND SCSI"
        elementNum += 1
    sys.exit()
except IOError as e:
    print "TRY AS vmx File"
    


try:
    expr5 = re.compile(r".*ide0:0.present");
    out = []
    with open(fileName+".vmx") as fp:
        for i, line in enumerate(fp):
            if expr5.findall(line) != []:
                temp = expr5.findall(line)
                out.append(temp[0])
    print " => " + str(out)
except IOError as e:
    print "MISSING VMX or OVF file"
    sys.exit()


















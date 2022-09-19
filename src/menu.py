import os
import sys
from datetime import datetime

class Menuitem:  
    def __init__(self, command, label, nbparams, jsonfile, isscreen,ret):  
        self.command = command
        self.label = label 
        self.nbparams = nbparams
        self.jsonfile = jsonfile
        self.isscreen =isscreen
        self.ret =ret
  
rootApp = os.getcwd()

def dotail(profil):       
    
    logFilename = f"{rootApp}{os.path.sep}log{os.path.sep}{profil}{dnow}.log"
    os.system (f"tail -f {logFilename}"

def kill():
    # kill them
    try:
        os.system ("killall /usr/lib/chromium-browser/chromium-browser")        
    except:
        pass


hardgreen="\033[32m\033[1m"
normalgreen="\033[32m\033[2m"
normalcolor="\033[0m"

def mencol(nb,fonc,comment):
    return f"{hardgreen}{normalcolor} - {nb} {hardgreen} - {comment}{normalcolor}"

def drkcol(str):    
    return f"{hardgreen}{str}{normalcolor}"

nbargs = len(sys.argv)
jsonfilefromarg = "default" if (nbargs == 1) else sys.argv[1]


clear = lambda : os.system('clear')
clear()
while True:
    
    print(drkcol("\n\nHi Neo, I'm the PyJobBot V1.1349"))
    print(drkcol("I'm ready to farm jobs"))
    print(drkcol("Your wish is my order\n\n"))
    print(drkcol("What I can do for you :\n\n"))

    menulist = []
    menulist.append(Menuitem("doreport","(see json file)",0,jsonfilefromarg,False,False))        
    menulist.append(Menuitem("test", "do test",0,jsonfilefromarg,False,False))     

    for idx,menuitem in enumerate(menulist): 
        print (mencol(idx,menuitem.command,menuitem.label))
        if menuitem.ret:print(drkcol("#####"))

    print (drkcol("#####"))
    print (mencol("55","tail","actual default log"))    
    print (mencol("94","editparams","edit default.json"))     
    print (mencol("97","kill","kill processes"))
    print (mencol("98","stop","stop current process"))
    print (mencol("99","exit","exit this menu"))
    dothat = input (drkcol("\n\nReady to farm : "))
    
    today = datetime.now()
    dnow = today.strftime(r"%y%m%d") 
    
    if dothat =="55":
        print(drkcol("\ntail -f default\n"))         
        dotail("default")
    if dothat =="94":
        print(drkcol("\edit params -r\n"))         
        os.system ("nano data/conf/default.json")     
    if dothat =="97":        
        print(drkcol("\nkill all\n"))         
        kill()
    if dothat =="98":
        print(drkcol("\nstop current process if exists\n"))
        os.system ("touch stop")
    if dothat == "99":
        print(drkcol("\nsee you soon, Neo\n"))
        quit()
    try:
        if int(dothat)<50:
            cmdstr="nop"    
        
            item =menulist[int(dothat)]
            cmd =item.command
            print (cmd)
            prms=int(item.nbparams)
            prmcmdlist=[]
            for i in range(prms):
                prmcmdlist.append(input (drkcol(f"enter param {i} :")))
            cmdstr=""
            if item.isscreen:cmdstr="screen "
            # calling the bot class would not help to test changes
            cmdstr += f"python3 run.py {cmd} {cmd}"
            for cmdarg in prmcmdlist:
                cmdstr+=f" {cmdarg}"
            print(cmdstr)
            os.system(cmdstr)
        
    except  Exception as e :
        print (e)
        print(f"\n{hardgreen}bad command (open your eyes){hardgreen}\n")

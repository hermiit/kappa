import json

datas = "./data/"

def printf(string,*argv):
   print(string % (argv))

def div():
   divstr = "---------------"
   print(divstr)
   return divstr

def parse(string):
   return str.split(string)
   
def first(string):
	return parse(string)[0]
   
def savejs(name,data):
   with open(datas+name+".json",'w') as openjs:
   	json.dump(data,openjs,indent=3)
   	
def getcmd(string):
   cmddict = None
   try:
      strcmd = first(string)
      cmdarr = parse(string)
      cmdpre = strcmd[:2]
      rcmd = strcmd[2:]
      with open(datas+'commands.json','r') as openjs:
   	   cmddict = json.load(openjs)
      
      if cmdpre == 'n:' and cmddict.get(rcmd):
         selcmd = cmddict.get(rcmd)
         return selcmd
   except IndexError:
      return False
      
def addbuild():
   botinfo = None
   with open(datas+"botinfo.json","r") as openjs:
      botinfo = json.load(openjs)
   
   botinfo["Build no."] += 1
   savejs("botinfo",botinfo)
   return botinfo["Build no."]

def getlist():
   with open(datas+'commands.json','r') as openjs:
      return json.load(openjs)
      
def getinfo():
   with open(datas+'botinfo.json','r') as openjs:
      return json.load(openjs)
   


                                                                                                                                                                      
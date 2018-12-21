#// Modules
import cmdmain
import discord
import asyncio
import time
import random
import math
import requests as reqs
import json
import thwiki
import nsave
from datetime import datetime,date
client = discord.Client()

pi = math.pi
sin = math.sin
token = "https://woah-ac6b3.firebaseio.com/nitori/users"
owner = "213839777840103426"
nico = "https://cdn.discordapp.com/attachments/512349953709047843/514307817486942211/67567-2.png"
logid = '523015818980753426'
datas = "./data/"
imgs = "./images/"
color = 0x00d0a0 # (0,208,160)

# get bot token
with open(datas+"thegoods.json") as sdat:
   token = (json.load(sdat)).get("token")

# main
@client.async_event
def on_message(message):
   if message.author == client.user:
      return

   maut = message.author
   mcon = message.content
   mchan = message.channel
   now = time.time()


   mtyp = client.send_typing
   msen = client.send_message
   mfil = client.send_file
   mdel = client.delete_message
   gmsg = client.get_message
   pmsg = cmdmain.parse(mcon)
   gcmd = cmdmain.getcmd(mcon)
   embo = None
   print(pmsg)

   nsave.saveuser({
      maut.id: {
         'name': maut.name,
         'nick': maut.nick,
         'id'  : maut.id,
         'avatar': maut.avatar
      }
   })

   # error message
   if gcmd:
      embo = discord.Embed(color=color)
      embo.title = "Incorrect command syntax."
      embo.description = "Usage: " + gcmd["usage"]

   ## the goods

   # n:help
   if gcmd and gcmd.get("name") == "help":
      pmsg = cmdmain.parse(mcon)
      cmddict = cmdmain.getlist()
      # infdict = cmdmain.getinfo()
      mtyp(mchan)

      cmdemb = discord.Embed(color=color)
      cmdemb.title = "Commands for Nitori"
      cmdemb.description = "Prefix: **n:**\n`<>` - Required parameter\n`()` - Optional parameter"
      cmddate = "Kappa | {0}".format(str(datetime.utcnow()))
      cmdemb.set_footer(text=cmddate,icon_url=nico)

      if len(pmsg) == 1:
         for cmd, items in cmddict.items():
            print(type(cmd))
            decstr = items.get("usage")
            cmdemb.add_field(name=items.get("name"),value=decstr,inline=False)
         yield from msen(mchan,embed=cmdemb)
      elif len(pmsg) == 2:
         try:
            if str.lower(pmsg[1]) == "raw":
               strcmd = json.dumps(cmddict,indent=3)
               msg = "Command .json:```json\n{}```".format(strcmd)
               yield from msen(mchan,content=msg)
            elif str.lower(pmsg[1]) == "rawfile":
               with open("./data/commands.json","r") as openjs:
                  msg = "Command .json file:"
                  yield from mfil(mchan,content=msg,fp=openjs)
            else:
               cmduse = None
               cmdnam = pmsg[1]
               for cmd, items in cmddict.items():
                  if cmd == str.lower(cmdnam):
                     cmduse = items.get("usage")
               shortemb = discord.Embed(color=color)
               shortemb.title = cmdnam
               shortemb.description = "Usage: " + cmduse
               yield from msen(mchan,embed=shortemb)
         except TypeError:
            msg = "Can't find that command, are you sure you typed it correctly?"
            yield from msen(mchan,content=msg)
         except IndexError:
            yield from msen(mchan,embed=embo)

   # n:info
   if gcmd and gcmd.get("name") == "info":
      infjs = cmdmain.getinfo()
      infmsg = discord.Embed(color=color)
      infmsg.title = "Bot Info"
      cmddate = "Kappa b. {:d} | {:s}".format(infjs["Build no."],str(datetime.utcnow()))
      infmsg.set_footer(text=cmddate,icon_url=nico)

      for name,inf in infjs.items():
         infmsg.add_field(name=name,value=str(inf),inline=False)
      yield from msen(mchan,embed=infmsg)

   # n:ping
   if gcmd and gcmd.get("name") == "ping":
      msg = "pong, {:s}. `{:.8g}`"
      yield from msen(mchan,content=msg.format(maut.mention,time.time()-now))

   # n:kick
   if gcmd and gcmd.get('name')  == 'kick' and maut.id == owner:
      first = None
      try:
         kuser = message.mentions[0]
         reason = '(none)'
         if len(pmsg) > 2:
            reason = ''
         if reason != '(none)':
            for i in range(2,len(pmsg)):
               print(pmsg[i])
               reason = reason + ' ' + pmsg[i]
         def check(msg):
            return msg.content.lower()
         first = "Attempting to kick user {:s}. Continue? (**Cancel** to cancel)".format(kuser.mention)
         first = yield from msen(mchan,content=first)
         msg = yield from client.wait_for_message(channel=mchan,author=maut,timeout=20,check=check)
         if msg.content.lower() in ['y','yes']:
            print('we got em')
            newk = kuser
            yield from client.kick(kuser)
            yield from mdel(first)
            embedo = discord.Embed(title='Banned user %s' % newk.name,color=color)
            embedo.add_field(name='Reason',value=reason,inline=False)
            embedo.add_field(name='ID',value='%s' % newk.id,inline=False)
            cmddate = "Kappa | {0}".format(str(datetime.utcnow()))
            embedo.set_footer(text=cmddate,icon_url=nico)
            yield from msen(client.get_channel(logid),embed=embedo,content='New kick from {:s}:'.format(maut.mention))
            if nsave.getuser(newk.id):
               print('Deleting userid %s...' % newk.id)
               print(reqs.delete('{:s}/{:s}.json'.format(nsave.blank,newk.id)))
      except IndexError:
         yield from msen(mchan,content='User not found.')
      except discord.errors.Forbidden:
         yield from mdel(first)
         yield from msen(mchan,content='I don\'t have the permissions for that, {:s}.'.format(maut.mention))


   # n:wiki
   if gcmd and gcmd.get("name") == "wiki":
      pmsg = cmdmain.parse(mcon)
      try:
         if len(pmsg) == 2:
            thget = thwiki.thsearch(pmsg[1])
            if thget[0][3] == []:
               msg = "No search results found."
               yield from msen(mchan,content=msg)
            else:
               msg = thget[0][1][0] + " | " + thget[0][3][0]
               yield from msen(mchan,content=msg)
         elif len(pmsg) == 3:
            thget = thwiki.thsearch(pmsg[1])
            rsnum = int(pmsg[2])
            if thget[0][3] == []:
               msg = "No search results found."
               yield from msen(mchan,content=msg)
            else:
               msg = thget[0][1][0] + " | " + thget[0][3][rsnum]
               yield from msen(mchan,content=msg)
         elif len(pmsg) == 1:
            msg = "Nitori (default search) | " + thwiki.thsearch("Nitori_Kawashiro")[0][3][0]
            yield from msen(mchan,content=msg)
         elif len(pmsg) > 3:
            msg = "Too many command parameters."
            yield from msen(mchan,content=msg)
      except IndexError:
         msg = "Result number was too high, try picking one <= 20."
         yield from msen(mchan,content=msg)
      except ValueError:
         msg = "Invalid page number, was it a normal integer?"

   # n:exit
   if gcmd and gcmd.get("name") == "exit":
      pmsg = cmdmain.parse(mcon)
      try:
         tout = float(pmsg[1])
         msg = yield from msen(mchan,content="*Exiting...*")

         time.sleep(tout)

         yield from mdel(msg)
         nsave.saveuser({},True)
         yield from client.logout()
      except ValueError:
         nsave.saveuser({},True)
         yield from client.logout()
      except IndexError:
         nsave.saveuser({},True)
         yield from client.logout()



@client.async_event
def on_ready():
   print("Build: " + str(cmdmain.addbuild()))
   print("Now we're cooking with gas!")


client.run(token)

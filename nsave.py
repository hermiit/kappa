import requests as reqs
import json
import time
import os

data = './data/'
userjs = data+'users.json'
blank = "https://woah-ac6b3.firebaseio.com/nitori/users"
api = blank + '.json'

cache = {}

def saveuser(vals={},force=False):
   cache.update(vals)
   if len(cache) >= 100 or force:
      dur = time.time()
      realjs = None
      print('Saving cache to disk...')
      with open(userjs,'r') as openjs:
         realjs = json.load(openjs)
         realjs.update(cache)
      with open(userjs,'w') as openjs:
         json.dump(realjs,openjs,indent=3,sort_keys=True)
      print('Cache saved!')
      cache.clear()
      print('Patching database...')
      with open(userjs) as openjs:
         usdict = json.load(openjs)
         usreq = reqs.patch(api,json=usdict)
         print(usreq)
      print('Data saved!')
      print('Total time: {:.3f}s | Size: {:d} bytes'.format(time.time()-dur,os.path.getsize(userjs)))

def getall():
   usreq = reqs.get(api)
   return usreq.json()

def getuser(id):
   users = getall()
   return users.get(id)

def parse(string):
   return str.split(string)
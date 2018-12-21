import requests

napi = "https://api.roblox.com"

def getuser(mode,v):
   if mode == 'id':
      usrget = requests.get(napi+'/users/'+v)
      getjs = usrget.json()
      return getjs
   elif mode == 'name':
      usrget = requests.get(napi+'/users/get-by-username',params={
         'user'
      })

getuser('id','261')
import requests as reqs
import time
from pybooru import Danbooru as dan

thapi = "https://en.touhouwiki.net/api.php"
danclient = dan("danbooru",username="crebb",api_key="X7w4ZdaB6ZKTqHHqPqXfMwfR")


def isnum(string):
   try:
      return int(string)
   except ValueError:
      return False

def thsearch(search):
   print("Searching info of %s..." % search)
   now = time.time()
   thget = reqs.get(url=thapi,params={
      "action": "opensearch",
      "search": search,
      "limit": 20
   })
   reqtime = time.time()-now
   print("Request time: " + str(reqtime))
   print(thget.status_code)
   # a good link is search[3][0]
   return [thget.json(),reqtime]
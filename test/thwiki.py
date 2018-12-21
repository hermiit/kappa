import requests as reqs

thapi = "https://en.touhouwiki.net/api.php"

def thsearch(search="Reimu"):
   thget = reqs.get(url=thapi,params={
      "action": "opensearch",
      "search": search,
      "limit": 5
   })
   return thget

newsearch = thsearch("Utsuho").json()

print(newsearch[3][0])
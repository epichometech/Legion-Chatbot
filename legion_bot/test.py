import urllib.request

req = urllib.request.Request(
  url = 'https://icanhazdadjoke.com/',
  headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'
    },
  method='GET')

with urllib.request.urlopen(req) as response:
  html = response.read()

print(html)
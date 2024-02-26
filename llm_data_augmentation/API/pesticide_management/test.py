########### Python 3.2 #############
import urllib.request, json

try:
    url = "https://api.datalake.sante.service.ec.europa.eu/sante/pesticides/active_substances?skip=0&take=100&substance_name=Fenhexamid&api-version=v1.0"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())
except Exception as e:
    print(e)
####################################
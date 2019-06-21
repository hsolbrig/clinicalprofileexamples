import requests
from jsonasobj import loads, as_json

resp = requests.get("http://hapi.clinicalprofiles.org/baseR4/Group/asthma-population?_pretty=true&_format=_json")
if resp.status_code == 200:
    asthma_pop = loads(resp.text)
    print(as_json(asthma_pop))
else:
    print(resp.reason)
print("X")

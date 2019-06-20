import requests
from jsonasobj import loads

url = "http://hapi.clinicalprofiles.org/baseR4/ClinicalProfile?_format=json&_count=10"
ids = []
while True:
    resp = requests.get(url)
    url = None
    if resp.status_code == 200:
        rslts = loads(resp.text)
        ids += [e.resource.id for e in rslts.entry]
        for l in rslts.link:
            if l.relation == "next":
                url = l.url
    if not url:
        break

print(f"Count: {len(ids)}")
print('\n'.join(sorted(ids)))
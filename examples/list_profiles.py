from typing import List, Tuple

import requests
from jsonasobj import loads

url = "http://hapi.clinicalprofiles.org/baseR4/ClinicalProfile?_format=json&_count=10"
ids:List[Tuple[str, str]] = []      # Tuples - cohort id to URL
while True:
    resp = requests.get(url)
    url = None
    if resp.status_code == 200:
        rslts = loads(resp.text)
        ids += [(e.resource.id, e.fullUrl) for e in rslts.entry]
        for l in rslts.link:
            if l.relation == "next":
                url = l.url
    else:
        print(resp.reason)
    if not url:
        break

print(f"Count: {len(ids)}")
print('\n'.join([e[0] + '\t' + e[1] for e in ids]))

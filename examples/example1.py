from jsonasobj import loads

import requests

resp = requests.get("http://hapi.clinicalprofiles.org/baseR4/ClinicalProfile/eds-All-All-All")
if resp.status_code  == 200:
    base = loads(resp.text)
resp = requests.get("http://hapi.clinicalprofiles.org/baseR4/ClinicalProfile/eds-All-All-10-19")
if resp.status_code == 200:
    var = loads(resp.text)
v1 = var.lab[0].scalarDistribution.decile
b1 = base.lab[0].scalarDistribution.decile
print(len(v1))
print(len(b1))
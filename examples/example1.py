from jsonasobj import loads

import requests

from examples.loinc_name import loinc_name_for

resp = requests.get("http://hapi.clinicalprofiles.org/baseR4/ClinicalProfile/eds-All-All-All")
if resp.status_code  == 200:
    base = loads(resp.text)
resp = requests.get("http://hapi.clinicalprofiles.org/baseR4/ClinicalProfile/eds-All-All-10-19")
if resp.status_code == 200:
    var = loads(resp.text)
var_codes = {l.code[0].coding[0].code: loinc_name_for(v.lab.code[0].coding[0].code) for v in var}


v1 = var.lab[0].scalarDistribution.decile
b1 = base.lab[0].scalarDistribution.decile
print(len(v1))
print(len(b1))
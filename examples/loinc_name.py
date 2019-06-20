from base64 import b64encode
from functools import lru_cache
from typing import Optional

import requests
from jsonasobj import loads, JsonObj


def map_parameters(struct) -> Optional[JsonObj]:
    if struct.resourceType == "Parameters":
        rval = JsonObj()
        for p in struct.parameter:
            if hasattr(p, 'valueString'):
                rval[p.name] = p.valueString
            elif hasattr(p, 'part'):
                rval[p.name] = p.part
            else:
                pass
        return rval
    return None


@lru_cache()
def loinc_name_for(code: str) -> str:
    userAndPass = b64encode(b"hsolbrig:instill-geminate-tehran").decode("ascii")
    headers = {'Authorization': 'Basic %s' % userAndPass}
    resp = requests.get(f"https://fhir.loinc.org/CodeSystem/$lookup?system=http://loinc.org&code={code}", headers=headers)
    if resp.status_code == 200:
        vals = map_parameters(loads(resp.text))
        if vals:
            return vals.display
        else:
            return "Unknown Code"


if __name__ == '__main__':
    print(loinc_name_for('4544-3'))

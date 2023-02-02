import os, time
import json, requests
import traceback

response = requests.get("http://192.168.0.28:32080/a1mediator/a1-p/policytypes/123/policies?policytype_id=123")

if response.status_code == 200:
    ins = response.text[5:-4]
    print(ins)

    response = requests.get(f"http://192.168.0.28:32080/a1mediator/a1-p/policytypes/123/policies/{ins}")

    if response.status_code == 200:
        if "ueId" in response.text:
            r = json.loads(response.text)["scope"]["qosId"]
            print(f"A1 Policy changed. qosId= {r}")
        else:
            print(response.text)
    else:
        print(response.text)

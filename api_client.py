import json
import requests
import time
import sys
import re
from requests.exceptions import ConnectTimeout, ReadTimeout

wait=5
debug=False

def fanIntersect(excr):
    if len(excr) > 1: print(excr)
    raise SystemExit(1)

if len(sys.argv) > 1 and re.fullmatch(r"[a-zA-Z0-9:/._-]+", sys.argv[1]):
    base_url = sys.argv[1]
else:
    print("Automated flag retrieval system v1.01\nPlease provide URL for API server as argument.")
    raise fanIntersect("")

def parseJSON(data):
    try:
        response = json.loads(data.text) 
    except:
        raise fanIntersect("JSON parser failed")   
    if isinstance(response, dict): 
        if debug == True: print(json.dumps(response, indent=2)) 
        return response
    else: raise fanIntersect("JSON parser failed") 

def apiREQ(req, content=None, headers=None, method="POST"):
    try:
        if debug == True: 
            print("REQ:",req,"CONTENT:", content, "HEADERS:", headers)
        if method == "POST":
            r = requests.post(base_url + req, json=content, headers=headers, timeout=wait)
        elif method == "GET":  
            r = requests.get(base_url + req, timeout=wait)
        content_type = str(r.headers.get("Content-Type"))
        status_code = int(r.status_code)
    except ReadTimeout, ConnectTimeout:
        raise fanIntersect("Connection time out")
    except RuntimeError, ValueError:
        raise fanIntersect("Request failed")
    except:
        raise fanIntersect(r'¯\(ツ)/¯')
    if status_code < 300 and "application/json" in content_type:
        return parseJSON(r)
    else:
        raise fanIntersect("invalid response")


def getToken():
    try: 
        t = apiREQ("api/token")
        token = str(t["token"])
    except:
        raise fanIntersect("token retrieval failed")
    if token.isalnum() and len(token) == 36:
        return token
    else:
        raise fanIntersect("token suspect")

def verifyToken(token):
    try:
        auth_header={"Authorization": f"Bearer {token}"}
        v = apiREQ("api/verify", headers=auth_header)
        secret_str = str(v.get("secret"))
    except:
            raise fanIntersect("Verification error")
    if secret_str.isalnum() and len(secret_str) == 32:
        secret = {"secret": secret_str}
        return (auth_header, secret)
    else:
        raise fanIntersect("secret suspect")

def claimFlag(verification):
    trust, verify = verification[::]
    try:
        f = apiREQ("api/flag", headers=trust, content=verify)
        flag = str(f.get("flag"))
    except:
        raise fanIntersect("flag waived")
    if len(flag) > 1 and re.fullmatch(r"[a-zA-Z0-9_{}-]+", flag):
        return flag
    else: raise fanIntersect("flag suspect")

def decorateFlag(flag):
    ornament  =  ""  + "*" * (len(flag)+4) + "\n"
    ornament +=  "*" + f" {flag} "         + "*\n"
    ornament +=  "*" * (len(flag)+4)       + "\n"
    return ornament

stopwatch = time.time()
                   
print(decorateFlag(claimFlag(verifyToken(getToken()))))

print(f"{(time.time() - stopwatch) * 1000:.0f}ms")
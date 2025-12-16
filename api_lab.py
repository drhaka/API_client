import json
import requests
import time
from requests.exceptions import ConnectTimeout, ReadTimeout

base_url = "http://10.3.10.104:3000/"
wait=5
debug=False

def fanIntersect(excr):
    print(excr)
    raise SystemExit(1)

def parseJSON(data):
    try:
        response: object = json.loads(data.text)   
        return response
    except:
        fanIntersect("JSON parser failed")   

def printResponse(sonjay):
    if isinstance(sonjay, dict):
        print(json.dumps(sonjay, indent=2))
    else:
        print(sonjay)    

def apiREQ(req, content=None, headers=None, method="POST"):
    try:
        if debug == True: 
            print("req:",req,"content:", content, "headers:", headers)
        if method == "POST":
            r = requests.post(base_url + req, json=content, headers=headers, timeout=wait)
        elif method == "GET":  
            r = requests.get(base_url + req, timeout=wait)
        if debug == True: 
            printResponse(parseJSON(r))
        content_type = str(r.headers.get("Content-Type"))
        status_code = int(r.status_code)
        if status_code < 300 and "application/json" in content_type:
            return parseJSON(r)
        else:
            raise RuntimeError
    except ReadTimeout:
        fanIntersect("Server timed out")
    except ConnectTimeout:
        fanIntersect("Connection timed out")
    except RuntimeError:
        fanIntersect("Invalid response")
    except:
        fanIntersect(r'¯\(ツ)/¯')
    
def getToken():
    token = apiREQ("api/token")
    if isinstance(token, dict):
        return str(token.get("token"))
    else:
        fanIntersect("token error")

def verifyToken(token):
    token_string = "Bearer " + str(token)
    auth_header={"Authorization": token_string}
    try:
        v = apiREQ("api/verify", headers=auth_header)
        secret = {"secret": str(v.get("secret"))}    
        return (auth_header, secret)
    except:
            fanIntersect("Verification error")

def claimFlag(verification):
    trust, verify = verification[::]
    try:
        response = apiREQ("api/flag",content=verify, headers=trust)
        flag = response.get("flag")
        return str(flag)
    except:
        fanIntersect("No claim")

def decorateFlag(flag):
    ornament = "\n" + "*" * (len(flag)+4) + "\n"
    ornament += "*" + f" {flag} " + "*\n"
    ornament += "*" * (len(flag)+4) + "\n"
    return str(ornament)

stopwatch = time.time()
                   
print(decorateFlag(claimFlag(verifyToken(getToken()))))

print(f"{(time.time() - stopwatch) * 1000:.0f}ms")
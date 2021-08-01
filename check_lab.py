#!//usr/bin/python3

import requests
import json
import os
import subprocess
from datetime import datetime

now = datetime.now()
timestamp = datetime.timestamp(now)

passcounter=0
failcounter=0
testcounter=0

testcounter +=1
url = "http://localhost:8001/services"
response = requests.request("GET", url)
if response.json()["data"][0]["name"] == 'mocking_service':
    passcounter +=1
else:
    failcounter +=1
    print("Service not configured")

testcounter +=1
url = "http://localhost:8001/routes"
response = requests.request("GET", url)
if response.json()["data"][0]["name"] == 'mocking':
    passcounter +=1
else:
    failcounter +=1
    print("Route not configured")

testcounter +=1
url = "http://localhost:8001/consumers"
response = requests.request("GET", url)
if response.json()["data"][0]["username"] == 'Jane':
    passcounter +=1
else:
    failcounter +=1
    print("Consumer not configured")

testcounter +=1
url = "http://localhost:8001/plugins"
response = requests.request("GET", url)
if response.json()["data"][0]["name"] == 'rate-limiting':
    passcounter +=1
else:
    failcounter +=1
    print("Plugin not configured")

testcounter +=1
url = "http://localhost:8000/mock/request"
response = requests.request("GET", url)
if response.status_code == 200:
    passcounter +=1
    print("Proxy request passed")
else:
    failcounter +=1
    print("Proxy request failed")

testcounter +=1
url = "http://localhost:8000/mock/request"
i = 6
while i > 0:
  response = requests.request("GET", url)
  i -= 1
if response.status_code == 429:
    passcounter +=1
else:
    failcounter +=1
    print("Plugin not configured correctly")

print("Number of tests: " + str(testcounter))
print("Number of Fails: " + str(failcounter))
print("Number of Passes: " + str(passcounter))

name = os.environ["AVL_STUDENT_ID"]
kongfilename = "env_" + name + "_" + str(timestamp) + "_kong.yaml"
envfilename = "kong_" + name + "_" + str(timestamp) + "_env.out"
subprocess.call(['deck', 'dump', '-o', kongfilename])

# env = os.environ
for k, v in os.environ.items():
    # print(f'{k}={v}')
    file = open(envfilename, "a")
    file.write(f'{k}={v}')
    file.write("\n")
    file.close

# https://www.tutorialspoint.com/python/python_sending_email.htm

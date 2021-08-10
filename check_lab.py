#!//usr/bin/python3

import requests
import json
import os
import subprocess
import tarfile
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")
studentemail = os.environ["AVL_STUDENT_ID"]
resultsfile = "results_" + studentemail + "_" + str(now) + "_results.out"

passcounter=0
failcounter=0
testcounter=0

testcounter +=1
url = "http://localhost:8001/services"
response = requests.request("GET", url)
try:
    if response.json()["data"][0]["name"] == 'mocking_service':
        passcounter +=1
    else:
        failcounter +=1
        print("'mocking_service' not configured")
        rf = open(resultsfile, "a")
        rf.write("'mocking_service' not configured\n")
        rf.close()
except:
    failcounter +=1
    print("Service not configured")
    rf = open(resultsfile, "a")
    rf.write("Service not configured\n")
    rf.close()

testcounter +=1
url = "http://localhost:8001/routes"
response = requests.request("GET", url)
try:
    if response.json()["data"][0]["name"] == 'mocking':
        passcounter +=1
    else:
        failcounter +=1
        print("Route '/mock' not configured")
        rf = open(resultsfile, "a")
        rf.write("Route '/mock' not configured\n")
        rf.close()
except:
    failcounter +=1
    print("Route not configured")
    rf = open(resultsfile, "a")
    rf.write("Route not configured\n")
    rf.close()

testcounter +=1
url = "http://localhost:8001/consumers"
response = requests.request("GET", url)
try:
    if response.json()["data"][0]["username"] == 'Jane':
        passcounter +=1
    else:
        failcounter +=1
        print("Consumer 'Jane' not configured")
        rf = open(resultsfile, "a")
        rf.write("Consumer 'Jane' not configured\n")
        rf.close()
except:
    failcounter +=1
    print("Consumer not configured")
    rf = open(resultsfile, "a")
    rf.write("Consumer not configured\n")
    rf.close()

testcounter +=1
url = "http://localhost:8001/plugins"
response = requests.request("GET", url)
try:
    if response.json()["data"][0]["name"] == 'rate-limiting':
        passcounter +=1
    else:
        failcounter +=1
        print("Plugin 'rate-limiting' not configured")
        rf = open(resultsfile, "a")
        rf.write("Plugin 'rate-limiting' not configured\n")
        rf.close()
except:
    failcounter +=1
    print("Plugin not configured")
    rf = open(resultsfile, "a")
    rf.write("Plugin not configured\n")
    rf.close()

testcounter +=1
url = "http://localhost:8000/mock/request"
response = requests.request("GET", url)
if response.status_code == 200:
    passcounter +=1
else:
    failcounter +=1
    print("Proxy request failed")
    rf = open(resultsfile, "a")
    rf.write("Proxy request failed\n")
    rf.close()

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
    rf = open(resultsfile, "a")
    rf.write("Plugin not configured correctly\n")
    rf.close()

print("Number of tests: " + str(testcounter))
print("Number of Fails: " + str(failcounter))
print("Number of Passes: " + str(passcounter))
percent = round(((passcounter) * 100) / testcounter)
print("Score: " + str(percent)  + "%")

resultsfile = "results_" + studentemail + "_" + str(now) + "_results.out"
rf = open(resultsfile, "a")
rf.write("Number of tests: " + str(testcounter) + '\n')
rf.write("Number of Fails: " + str(failcounter) + '\n')
rf.write("Number of Passes: " + str(passcounter) + '\n')
rf.write("Score: " + str(percent)  + "%")
rf.close()

kongfile = "kong_" + studentemail + "_" + str(now) + "_kong.yaml"
subprocess.call(['deck', 'dump', '-o', kongfile])

envfile = "env_" + studentemail + "_" + str(now) + "_env.out"
for k, v in os.environ.items():
    # print(f'{k}={v}')
    file = open(envfile, "a")
    file.write(f'{k}={v}')
    file.write("\n")
    file.close

studentname = studentemail.split("@")[0]
tarfilename = "labfiles_" + studentname + "_" + str(now) + ".tar.gz"
tf = tarfile.open(tarfilename, mode="w:gz")
tf.add(kongfile)
tf.add(envfile)
tf.add(resultsfile)
tf.close()


# https://www.tutorialspoint.com/python/python_sending_email.htm

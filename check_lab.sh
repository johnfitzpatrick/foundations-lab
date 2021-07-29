#!/bin/bash

passcounter=0
failcounter=0
testcounter=0

deck dump

# Check services
# SERVICE=$(curl -s -X GET http://localhost:8001/services | jq '.data[].name' | xargs)
testcounter=$((testcounter+1))
if [[ $(curl -s -X GET http://localhost:8001/services | jq '.data[].name' | xargs) = mocking_service ]]; then
  passcounter=$((passcounter+1))
else
  failcounter=$((failcounter+1))
  echo Service not configured
fi


testcounter=$((testcounter+1))
if [[ $(curl -s -X GET http://localhost:8001/routes | jq '.data[].name' | xargs) = mocking ]]; then
  passcounter=$((passcounter+1))
else
  failcounter=$((failcounter+1))
  echo Route not configured
fi

# Check consumers

testcounter=$((testcounter+1))
if [[ $(curl -s -X GET http://localhost:8001/consumers | jq '.data[].username' | xargs) = Jane ]]; then
  passcounter=$((passcounter+1))
else
  failcounter=$((failcounter+1))
  echo Consumer not configured
fi

# Check plugins
testcounter=$((testcounter+1))
if [[ $(curl -s -X GET http://localhost:8001/plugins | jq '.data[].name' | xargs) = rate-limiting ]]; then
  passcounter=$((passcounter+1))
else
  failcounter=$((failcounter+1))
  echo Plugin not configured
fi

# Validate Rate Limiting - run the following 6 times and you should see 'API rate limit exceeded'
for i in {1..6}; do curl -s -i -X GET http://localhost:8000/mock/request > /dev/null; done
testcounter=$((testcounter+1))
if [[ $(curl -s -I -X GET http://localhost:8000/mock/request | head -n 1 | awk '{print $2}') = 429 ]]; then
  passcounter=$((passcounter+1))
else
  echo Plugin not working as planned
  failcounter=$((failcounter+1))
fi

percent=$(($passcounter*100/$testcounter))
echo $testcounter tests run, $passcounter passed and $failcounter failed. $percent% pass rate.

echo Resetting Kong Gateway
yes | deck reset

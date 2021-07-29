#!/bin/bash

yes | deck reset
bash -c 'sleep 10; ./check_lab.sh' &

#
# # Create a service
# curl -i -X POST http://localhost:8001/services \
#   --data name=mocking_service \
#   --data url='http://mockbin.org'
#
# # Create a route
# curl -i -X POST http://localhost:8001/services/mocking_service/routes \
#   --data name=mocking \
#   --data 'hosts=localhost' \
#   --data 'paths[]=/mock'
#
# # Verify the route
# curl -i -X GET http://localhost:8000/mock/request
#
# # Create a new consumer called 'Jane'
# curl -X POST http://localhost:8001/consumers  -d "username=Jane"
# curl -X GET http://localhost:8001/consumers | jq
#
#
# # Configure 'rate-limiting' plugin
# curl -i -X POST http://localhost:8001/plugins \
#   --data name=rate-limiting \
#   --data config.minute=5 \
#   --data config.policy=local
#
#
# # Validate Rate Limiting - run the following 6 times and you should see 'API rate limit exceeded'
# # curl -i -X GET http://localhost:8000/mock/request
# for i in {1..6}; do curl -s -i -X GET http://localhost:8000/mock/request| head -n 1; done
# curl -s -I -X GET http://localhost:8000/mock/request | head -n 1
#
#
# # List all Services & Plugins
# curl -X GET http://localhost:8001/services | jq
# curl -X GET http://localhost:8001/plugins | jq

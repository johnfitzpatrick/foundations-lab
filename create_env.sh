#!/bin/bash

yes | deck reset

# Create a service
curl -i -X POST http://localhost:8001/services \
  --data name=mocking_service \
  --data url='http://mockbin.org'

# Create a route
curl -i -X POST http://localhost:8001/services/mocking_service/routes \
  --data name=mocking \
  --data 'hosts=localhost' \
  --data 'paths[]=/mock'


# Create a new consumer called 'Jane'
curl -X POST http://localhost:8001/consumers  -d "username=Jane"


# Configure 'rate-limiting' plugin
curl -i -X POST http://localhost:8001/plugins \
  --data name=rate-limiting \
  --data config.minute=5 \
  --data config.policy=local

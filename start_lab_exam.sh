#!/bin/bash

yes | deck reset > /dev/null

# 20mins is 1200 seconds. Setting to 10 secs for testing
bash -c 'sleep 10; ./check_lab.sh' &

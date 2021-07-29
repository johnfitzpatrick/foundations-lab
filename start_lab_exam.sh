#!/bin/bash

yes | deck reset > /dev/null
bash -c 'sleep 10; ./check_lab.sh' &

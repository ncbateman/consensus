#!/bin/bash

# Start the cron service
service cron start

# Keep the container running by tailing a log file
tail -f /dev/null

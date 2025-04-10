#!/bin/bash

# URL to test
URL="http://url-shortener.local/shorten"

# JSON payload for the request
PAYLOAD='{"url":"https://amazon.in"}'

# Number of requests to make
NUM_REQUESTS=1000

# Number of concurrent requests
CONCURRENCY=50

# Create the payload file first
echo $PAYLOAD > payload.json

# Run the test
echo "Starting stress test with $NUM_REQUESTS requests and $CONCURRENCY concurrent connections"
ab -n $NUM_REQUESTS -c $CONCURRENCY -p payload.json -T 'application/json' $URL
#!/bin/bash

SECONDS=0
echo "Starting unittest....."
python3 -m test.test_movie_collection
echo "Unittests completed. "
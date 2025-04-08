#!/bin/bash

# Kill any existing Flask processes
pkill -f "python3.*flask"
pkill -f "python.*server.py"
sleep 2  # Give processes time to clean up

# Start the server (which now includes registering the cluster album builder API)
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 backend/server.py 
#!/bin/bash

kill -9 $(ps aux | grep -v grep | grep "record_data.py" | awk '{print $2}')

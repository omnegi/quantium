#!/bin/bash

source venv/Scripts/activate

pytest test/ -v

if [ $? -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Tests failed."
    exit 1
fi


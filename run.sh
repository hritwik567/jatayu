#!/bin/bash
cd $1
nohup python3.6 app.py 1>log 2>err &

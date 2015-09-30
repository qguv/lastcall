#!/bin/bash

docker build -t lastcall . &&
docker run lastcall

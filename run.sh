#!/bin/bash

docker build -t lastcall . &&
docker run -p 80:80 lastcall $@

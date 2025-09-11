#!/bin/bash

docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock dslim/slim build pfa-manager-api:latest

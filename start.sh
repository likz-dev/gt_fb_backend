#!/bin/bash
app="gt_backend.test"
docker build --no-cache -t ${app} .
docker run -d -p 80:80 ${app}
#!/bin/bash
# need to set ALL ALL = NOPASSWD: /usr/bin/mem_util.sh
timestamp=$(date +%y%m%dT%H%M)

which smem > /dev/null 2>&1
if [ $? -ne 0 ]
then
    sudo dnf install -qy smem
fi

sudo mkdir -p /var/log/mem_util/
smem -tk > /var/log/mem_util/$timestamp.log
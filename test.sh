#!/bin/sh

delay=0
timeunit="ms"
for i in {1..5}
do
    ((delay+=50))
    echo "tc qdisc add dev eth0 root netem delay $delay$timeunit"
    sleep 1
done
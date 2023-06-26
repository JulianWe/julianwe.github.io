#!/bin/bash
for i in {1..1000} 
do
sentinelcli query subscriptions \
    --home sentinelcli \
    --node https://rpc.sentinel.co:443 \
    --page "$i" | grep sent1srujzhj2v9fkzhnn635udlczyhdpetuh84qfqc
done

#!/bin/sh

timeout 20m redis-benchmark -h 34.132.63.119 -n 1000 -c 100 -d 10 -t get,set -l --csv > redis_benchmark_linear_network_delay.csv
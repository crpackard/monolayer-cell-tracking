#!/bin/bash
for ii in $(seq 2 5); do
  nohup python3.9 parallelize.py $ii &
done

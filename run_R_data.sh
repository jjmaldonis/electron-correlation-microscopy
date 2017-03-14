#!/bin/bash

ls -l
echo $@

wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/python.tar.gz
tar -xzf python.tar.gz
rm python.tar.gz
export PATH=$(pwd)/python/bin:$PATH

# Setup for script
mkdir R2xy_data
mkdir "R2xy_data/R=$@.0"

# run your script
python create_R_data.py $@

mv R2xy_data/* .
tar -zcvf R=$@.0.tar.gz R\=$@.0/

rm -rf python R2xy_data

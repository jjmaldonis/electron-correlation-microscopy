#!/bin/bash

ls -l
echo $@

wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/python.tar.gz
wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/tif_C242.tar.gz

# untar your Python installation and other necessary files
tar -xzf python.tar.gz
tar -xzf tif_C242.tar.gz

#rm anaconda2.tar.gz
rm python.tar.gz
rm tif_C242.tar.gz

# make sure the script will use your Python installation
export PATH=$(pwd)/python/bin:$PATH

# Setup for script
mkdir spatial_results
cd R2xy_data
tar -xf R=10.0.tar.gz
tar -xf R=1.0.tar.gz
tar -xf R=2.0.tar.gz
tar -xf R=3.0.tar.gz
tar -xf R=4.0.tar.gz
tar -xf R=5.0.tar.gz
tar -xf R=6.0.tar.gz
tar -xf R=7.0.tar.gz
tar -xf R=8.0.tar.gz
tar -xf R=9.0.tar.gz
rm -rf R*.tar.gz
cd ../

# run your script
python g4spatial_unaveraged.py $@


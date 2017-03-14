#!/bin/bash

ls -l
echo $@

wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/python.tar.gz
wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/tif_C238_2.tar.gz

# untar your Python installation and other necessary files
tar -xzf python.tar.gz
tar -xzf tif_C238_2.tar.gz

#rm anaconda2.tar.gz
rm python.tar.gz
rm tif_C238_2.tar.gz

# make sure the script will use your Python installation
export PATH=$(pwd)/python/bin:$PATH

# Setup for script
mkdir spatial_results
cd R2xy_data
for filename in *.tar.gz
do
  tar -xf $filename
done
rm -rf R*.tar.gz
cd ../

# run your script
python g4spatial_unaveraged.py $@

rm -rf R2xy_data

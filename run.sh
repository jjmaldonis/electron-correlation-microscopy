#!/bin/bash

ls -l
echo $@

#wget http://proxy.chtc.wisc.edu/SQUID/maldonis/anaconda2.tar.gz
wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/python.tar.gz
wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/tif_C234.tar.gz

# untar your Python installation and other necessary files
#tar -xf anaconda2.tar.gz
tar -xzf python.tar.gz
tar -xzf tif_C234.tar.gz

#rm anaconda2.tar.gz
rm python.tar.gz
rm tif_C234.tar.gz

# make sure the script will use your Python installation
#export PATH=$(pwd)/anaconda2/bin:$PATH
export PATH=$(pwd)/python/bin:$PATH

#wget https://bootstrap.pypa.io/get-pip.py
#python get-pip.py
#pip install conda
#conda create -n py3 --file exported.txt
#source activate py3

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
# The above command should create an (x,y).data image

#rm -rf python tif R2xy_data  # Since these are dirs, they won't be transfered back anyways


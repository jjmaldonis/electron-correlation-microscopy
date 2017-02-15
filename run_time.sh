#!/bin/bash

ls -l
echo $@

#wget http://proxy.chtc.wisc.edu/SQUID/maldonis/anaconda2.tar.gz
wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/python.tar.gz
wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/tif-20161209T184603Z.zip

# untar your Python installation and other necessary files
#tar -xf anaconda2.tar.gz
tar -xzf python.tar.gz
unzip -q tif-20161209T184603Z.zip

#rm anaconda2.tar.gz
rm python.tar.gz
rm tif-20161209T184603Z.zip

# make sure the script will use your Python installation
#export PATH=$(pwd)/anaconda2/bin:$PATH
export PATH=$(pwd)/python/bin:$PATH

#wget https://bootstrap.pypa.io/get-pip.py
#python get-pip.py
#pip install conda
#conda create -n py3 --file exported.txt
#source activate py3

# Setup for script
#mkdir spatial_results
#mkdir R2xy_data
#mv R*.tar.gz R2xy_data/
#cd R2xy_data
#tar -xvf R*.tar.gz
#mv R*/* .
#rm -rf R*.tar.gz
#cd ../

# run your script
python g4.py $@

#mv spatial_results/* .

#rm -rf anaconda2 tif R2xy_data
rm -rf python tif


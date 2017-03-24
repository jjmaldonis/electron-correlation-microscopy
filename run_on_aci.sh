if [ -z "$1" ]; then
    echo "Pass in a paramfile"
    exit 1
fi

git pull
source activate structopt3 && module load compile/intel mpi/intel/openmpi-1.10.2 

python setup.py $1

DSKEY="$(python get_dataset_key.py $1)"

#wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/tif_${DSKEY}.tar.gz
#tar -xzf tif_${DSKEY}.tar.gz

python create_R_data.py $1

python g4spatial.py $1

#python g2time.py $1

#python g2spatial.py $1


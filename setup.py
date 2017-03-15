import json
import os
import subprocess


params = json.load(open("parameters.json"))



# Make a bunch of directories for storing the results
for direc in ["results", "results/{}".format(params["dataset_key"})]]:
    if not os.path.exists(direc):
        os.path.makedirs(direc)
for direc in ["results/{}/R2xy_data/{}".format(params["dataset_key"}, R)] for R in range(*params["dr_range"])]:
    if not os.path.exists(direc):
        os.path.makedirs(direc)


# This should pull the *.tar.gz from squid and untar it, revealing the "tif" folder
# The mask must already be in place
subprocess.call(["setup_py.sh", params["dataset_key"]])


run_g4_spatial = """
#!/bin/bash

ls -l
echo $@

wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/python.tar.gz
tar -xzf python.tar.gz
rm python.tar.gz
export PATH=$(pwd)/python/bin:$PATH

wget -q http://proxy.chtc.wisc.edu/SQUID/maldonis/tif_{key}.tar.gz
tar -xzf tif_{key}.tar.gz
rm tif_{key}.tar.gz

# Setup for script
mkdir spatial_results
cd R2xy_data
for filename in *.tar.gz
do
  tar -xf $filename
done
rm -rf R*.tar.gz
cd ../

python g4spatial.py $@

rm -rf R2xy_data
""".format(key=params["dataset_key"])
with open("run_spatial.sh", "w") as f:
    f.write(run_g4_spatial)


submit_osg = """
universe = vanilla

requirements = (OpSys == "LINUX") && (OpSysMajorVer == 6)

+WantFlocking = true
+WantGlidein = true

executable = run_spatial.sh
arguments = $(X) $(Y)

output = $(Cluster)_$(Process).out
error = $(Cluster)_$(Process).err
log = $(Cluster).log

should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = run.sh, g4spatial.py, utilities.py, mask_{key}.txt, R2xy_data

request_cpus = 1
request_memory = 2400MB
request_disk = 4GB

queue X, Y from inputs1.in
""".format(key=params["dataset_key"])
with open("submit_osg.sub", "w") as f:
    f.write(submit_osg)




submit_Rs = """
universe = vanilla

requirements = (OpSys == "LINUX") && (OpSysMajorVer == 6)

executable = run_R_data.sh
arguments = $(R)

output = $(Cluster)_$(Process).out
error = $(Cluster)_$(Process).err
log = $(Cluster).log

should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = run_R_data.sh, create_R_data.py, utilities.py, mask_{key}.txt

request_cpus = 1
request_memory = 2400MB
request_disk = 4GB

queue R from input_Rs.in
""".format(key=params["dataset_key"])
with open("submit_Rs.sub", "w") as f:
    f.write(submit_Rs)



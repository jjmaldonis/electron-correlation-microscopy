import json


params = json.load(open("parameters.json"))


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

python g4spatial_unaveraged.py $@

rm -rf R2xy_data
""".format(key=params["dataset_key"])
with open("run_spatial.sh", "w") as :
    f.write(run_g4_spatial)


submit_osg = """
universe = vanilla

requirements = (OpSys == "LINUX") && (OpSysMajorVer == 6)

+WantFlocking = true
+WantGlidein = true

executable = run.sh
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
with open("submit_osg.sub", "w") as :
    f.write(submit_osh)





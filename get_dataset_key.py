import json
import sys

paramfile = sys.argv[1]
params = json.load(open(paramfile))
print(params["dataset_key"])

from root_numpy import root2array, tree2array
from root_numpy import testdata
import numpy as np

filename = "/lustre/cmswork/hh/alp_moriond_base/def_cmva/BTagCSVRun2016.root"

# Convert a TTree in a ROOT file into a NumPy structured array
arr = root2array(filename, 'pair/tree', 
	branches=['EventInfo.run_', 'lumiBlock_', 'event_']
)
# The TTree name is always optional if there is only one TTree in the file

np.savetxt("events.txt", arr, delimiter=":", fmt='%u')

from test import *
from train import train_nn_model
from utils import *
from pointData import PointFeatures, SampleSet
import numpy as np 

FILEPATH_SAMPLE = 'data/top_data.xls'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'
ROOT_PATH = 'nn_models/removed2'
BOUNDARY_TR = [8000,13400,3800,5850]
BOUNDARY_TEST = [3500,6500,1000,3000]

if __name__ == "__main__":
	my_set = SampleSet(FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY_TR)
	my_data = my_set.points
	xlist,ylist,matrix,ty = pre_training_set(my_data)
	train_nn_model(matrix,ty)
	pys,names = test_model_in_file(matrix,ROOT_PATH)
	#print(ty,py)
	#print_compared_mental_map(xlist,ylist,ty,py)
	pys.append(ty)
	names.append('training_set')
	print_all_mental_maps(xlist,ylist,pys,names)
	dump_to_excel(names,pys)

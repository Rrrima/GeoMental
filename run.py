from test import *
from train import train_nn_model
from utils import *
from pointData import PointFeatures, SampleSet
import numpy as np
from name_generator import generate_names
from analysis import *

FILEPATH_SAMPLE = 'data/top_data.xls'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'
ROOT_PATH = 'nn_models/removed2'
BOUNDARY_TR = [8000,13400,3800,5850]
BOUNDARY_TEST = [3500,6500,1000,3000]
OUT_NAME = '11_16_11_40.xls'

def create_vector():
	my_set = SampleSet(FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY_TEST)
	my_data = my_set.points
	xlist,ylist,matrix,ty = pre_training_set(my_data)
	ATT_NAMES = generate_names()
	#num_att = len(matrix[0])
	print(ATT_NAMES)
	dump_to_excel_attributes(xlist,ylist,ATT_NAMES,matrix,ty,OUT_NAME)
def analysis_vector():
	ATT_NAMES = generate_names()
	size_trend_analysis(OUT_NAME,ATT_NAMES)

if __name__ == "__main__":
	# get nn_models training here
	# train_nn_model(matrix,ty)
	# pys,names = test_model_in_file(matrix,ROOT_PATH)
	# print(ty,py)
	# print_compared_mental_map(xlist,ylist,ty,py)
	# pys.append(ty)
	# names.append('training_set')
	# print_all_mental_maps(xlist,ylist,pys,names)
	# dump_to_excel(names,pys) 
	analysis_vector()
	
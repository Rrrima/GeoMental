# test classes 
# REMOVE it from the final project
import pprint
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from collections import defaultdict

np.set_printoptions(threshold=np.inf)
pp = pprint.PrettyPrinter(indent=4)
from utils import *

FILEPATH_SAMPLE = 'data/top_data.xls'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'
BOUNDARY = [8000,13400,3800,5850]

from pointData import PointFeatures, SampleSet

if __name__ == "__main__":
	my_set = SampleSet(FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY)
	my_data = my_set.points
	# plot points
	'''
	xlist = [data.x for data in my_data]
	ylist = [data.y for data in my_data]
	clist = [tuple([x/255 for x in data.rgb]) for data in my_data]
	for data in my_data:
		print(data.vector,data.Cr)
	print (my_set.rgb_labels)
	plt.scatter(xlist, ylist, c=clist, alpha = 0.6)
	plt.show()
	'''
	matrix,ty = pre_training_set(my_data)
	#pp.pprint (matrix)
	#pp.pprint(ty)
	params_dict = defaultdict(int)
	for hls in [3,10,20,50,100]:
		for alp in [0.5,0.001,0.0001,0.00001]:
			for mi in [100,200,500,1000]:
				best_index = 0
				min_loss = 99999999
				current_index = 0
				while(current_index<300):
					nn_result = MLPRegressor(hidden_layer_sizes=hls, alpha =alp, max_iter=mi).fit(matrix,ty)
					if min_loss>nn_result.loss_:
						best_index = current_index
						min_loss = nn_result.loss_
					current_index += 1
				print(min_loss)
				this_key = str(hls)+str(alp)+str(mi)
				params_dict[this_key] = min_loss

	print (params_dict)


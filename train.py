# test classes 
# REMOVE it from the final project
import pprint
import numpy as np
import matplotlib.pyplot as plt
from joblib import dump
from os import path
from sklearn.neural_network import MLPRegressor
from collections import defaultdict

np.set_printoptions(threshold=np.inf)
pp = pprint.PrettyPrinter(indent=4)
from utils import *

def train_nn_model(matrix,ty):
	# train using nn
	params_dict = defaultdict(int)
	for hls in [10]:
		for alp in [0.0001]:
			for mi in [2000]:
				best_index = 0
				min_loss = 99999999
				current_index = 0
				while(current_index<1000):
					nn_result = MLPRegressor(hidden_layer_sizes=hls, alpha =alp, max_iter=mi).fit(matrix,ty)
					print(nn_result.loss_)
					if min_loss>nn_result.loss_:
						best_index = current_index
						min_loss = nn_result.loss_
						best_model = nn_result
					current_index += 1
				print(min_loss)
				this_key = str(hls)+'-'+str(alp)+'-'+str(mi)
				params_dict[this_key] = min_loss
				dump(best_model, path.join('nn_models','removed',this_key+'-'+str(int(min_loss))+'.joblib')) 
	print (params_dict)
	


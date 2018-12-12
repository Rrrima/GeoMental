import xlrd
import pprint
import numpy as np 
from scipy.spatial import distance


pp = pprint.PrettyPrinter(indent=4)
# x:latitude
# y:longtitude

def get_sampling_points(filePath):
	data = []
	book = xlrd.open_workbook(filePath)
	table = book.sheets()[0]
	nrows = table.nrows
	for i in range(1,nrows):
		data.append(table.row_values(i))
	return data

def get_std(arr):
	return np.std(arr)

def eu_distance(a,b):
	return distance.euclidean(a, b)

def pre_training_set(data,size=None):
	matrix = []
	target = []
	if size is None:
		size = len(data)
		for i in range(size):
			ty = data[i].Cr
			if ty!='':
				matrix.append(data[i].vector)
				target.append(data[i].Cr)
	return matrix,target
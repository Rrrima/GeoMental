# test classes 
# REMOVE it from the final project
import pprint
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)
pp = pprint.PrettyPrinter(indent=4)

FILEPATH_SAMPLE = 'data/top_data.xls'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'
BOUNDARY = [8000,13400,3800,5850]

from pointData import PointFeatures, SampleSet

if __name__ == "__main__":
	my_set = SampleSet(FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY)
	my_data = my_set.points
	# plot points
	xlist = [data.x for data in my_data]
	ylist = [data.y for data in my_data]
	clist = [tuple([x/255 for x in data.rgb]) for data in my_data]
	for data in my_data:
		print(data.vector,data.Cr)
	print (my_set.rgb_labels)
	plt.scatter(xlist, ylist, c=clist, alpha = 0.6)
	plt.show()

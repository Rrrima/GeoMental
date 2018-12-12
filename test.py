# test classes 
# REMOVE it from the final project
import pprint
import numpy as np
np.set_printoptions(threshold=np.inf)
pp = pprint.PrettyPrinter(indent=4)

FILEPATH_SAMPLE = 'data/top_data.xls'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'


from pointData import PointFeatures, SampleSet

if __name__ == "__main__":
	my_set = SampleSet(FILEPATH_SAMPLE, FILEPATH_MAP)
	my_data = my_set.points
	for data in my_data:
		print(data.vector,data.Cr)
	print (my_set.rgb_labels)

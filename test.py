# test classes 
# REMOVE it from the final project
import pprint
pp = pprint.PrettyPrinter(indent=4)

FILEPATH_SAMPLE = 'data/top_data.xls'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'


from pointData import PointFeatures, SampleSet

if __name__ == "__main__":
	my_data = SampleSet(FILEPATH_SAMPLE, FILEPATH_MAP)
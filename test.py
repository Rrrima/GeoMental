# test classes 
# REMOVE it from the final project
FILEPATH_SAMPLE = 'top_data.xls'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'

from geoMap import GeoMap

if __name__ == "__main__":
	my_map = GeoMap(FILEPATH_MAP)
	print(my_map.x0)
	print(my_map.get_pixel_value(2939,1232))
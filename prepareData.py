from osgeo import gdal
from collections import defaultdict
import math

gdal.AllRegister()


# rotation is not considered
# make sure rx = ry = 0
def get_data_from_tif(filePath,left=4000,right=4100,bottom=4000,top=4100):

	data = get_tif_info(filePath)
	band_set = data['band_set']
	p_width = data['p_width']
	p_height = data['p_height']
	pixel_set = []
	print(band_set)
	for i in range(bottom,top):
		row = []
		for j in range(left,right):
			point_value = [] 
			for single_band in band_set:
				print(single_band.ReadAsArray(1,1,1,1))
				#point_value.extend(single_band.ReadAsArray(j,i,1,1))

			row.append(point_value)
			print(point_info)
		pixel_set.append(row)
	return pixel_set






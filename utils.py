import xlrd
import pprint
from osgeo import gdal
import GeoMap

pp = pprint.PrettyPrinter(indent=4)
# x:latitude
# y:longtitude

def convert_point(map,x,y):
	map_info = get_tif_info(map)
	x0 = map.x0
	y0 = map.y0
	pw = map.pixel_width
	ph = map.pixel_height
	return int((x-x0)/pw),int((y-y0)/ph)	

def get_sampling_point(filePath):
	data = []
	book = xlrd.open_workbook(filePath)
	table = book.sheets()[0]
	nrows = table.nrows
	for i in range(1,nrows):
		this_point = table.row_values(i)
		if ((this_point[0]>0) & (this_point[1]>0)):
			data.append()
	pp.pprint(data)
	return data

def get_map_bandvalue(file)


FILEPATH_SAMPLE = 'top_data.xls'
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'
get_sampling_point(FILEPATH_SAMPLE)
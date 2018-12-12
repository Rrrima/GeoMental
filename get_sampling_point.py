import xlrd
import pprint
from osgeo import gdal

pp = pprint.PrettyPrinter(indent=4)
# x:latitude
# y:longtitude
def get_tif_info(filePath):
	f = filePath
	data = gdal.Open(f)
	adf = data.GetGeoTransform()
	rx = adf[2]
	ry = adf[4]
	nX = data.RasterXSize
	nY = data.RasterYSize
	nB = data.RasterCount
	band_set = []
	for i in range(nB):
		band_set.append(data.GetRasterBand(i+1))

	return {
		'nx':nX,
		'ny':nY,
		'x0':adf[0],
		'y0':adf[3],
		'p_width':adf[1],
		'p_height':adf[5],
		'band_set':band_set
	}

def convert_point(map,x,y):
	map_info = get_tif_info(map)
	x0 = map_info['x0']
	y0 = map_info['y0']
	pw = map_info['p_width']
	ph = map_info['p_height']
	return int((x-x0)/pw),int((y-y0)/ph)	

def get_sampling_point(filePath):
	data = []
	book = xlrd.open_workbook(filePath)
	table = book.sheets()[0]
	nrows = table.nrows
	for i in range(1,nrows):
		this_point = table.row_values(i)
		converted_cord = convert_point(FILEPATH_MAP,this_point[0],this_point[1])
		this_point[0] = converted_cord[0]
		this_point[1] = converted_cord[1]
		if ((this_point[0]>0) & (this_point[1]>0)):
			data.append(this_point)
	pp.pprint(data)
	return data

def get_map_bandvalue(file)


FILEPATH_SAMPLE = 'top_data.xls'
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'
get_sampling_point(FILEPATH_SAMPLE)
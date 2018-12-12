# class for PointFeatures
from utils import *
from geoMap import GeoMap


class PointFeatures(object):
	def __init__(self, data, value):
		# data: data in row from xls
		self._map = map
		self._x = data[0]
		self._y = data[1]
		self._pH = data[2]
		self._Cr = data[3]
		self._Ni = data[4]
		self._Cu = data[5]
		self._Zn = data[6]
		self._Cd = data[7]
		self._Pb = data[8]
		self._As = data[9]
		self._Hg = data[10]
		self._value = value

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def value(self):
		return self._value

	@property
	def Cr(self):
		return self._Cr
	

class SampleSet(object):
	def __init__(self, dataPath, mapPath)
		self._map = GeoMap(mapPath)
		self._origin_points = get_sampling_points(dataPath)
		self._size = len(self._origin_points)
		self._points = self._create_points()

	@property
	def size(self):
		return self._size
	
	def _convert_point(self,x,y):
		ref_map = self._map
		x0 = ref_map.x0
		y0 = ref_map.y0
		pw = ref_map.pixel_width
		ph = ref_map.pixel_height
		return int((x-x0)/pw),int((y-y0)/ph)

	def _create_points(self):



for i in range(1,nrows):
		this_point = table.row_values(i)
		converted_cord = convert_point(FILEPATH_MAP,this_point[0],this_point[1])
		this_point[0] = converted_cord[0]
		this_point[1] = converted_cord[1]
		if ((this_point[0]>0) & (this_point[1]>0)):
			data.append(this_point)
	pp.pprint(data)
	return data
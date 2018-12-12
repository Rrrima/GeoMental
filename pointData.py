# class for PointFeatures
from utils import *
from geoMap import GeoMap


class PointFeatures(object):
	def __init__(self, data, map):
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
		self._value = map.get_pixel_value(self._x,self._y)

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
	def __init__(self, dataPath, mapPath):
		self._map = GeoMap(mapPath)
		self._origin_points = get_sampling_points(dataPath)
		self._size = len(self._origin_points)
		self._featured_points = self._create_points()

	@property
	def size(self):
		return self._size

	@property
	def points(self):
		return self._featured_points
	
	
	def _convert_point(self,x,y):
		ref_map = self._map
		x0 = ref_map.x0
		y0 = ref_map.y0
		pw = ref_map.pixel_width
		ph = ref_map.pixel_height
		return int((x-x0)/pw),int((y-y0)/ph)

	def _create_points(self):
		points = []
		boundx = self._map.xsize
		boundy = self._map.ysize
		for i in range(self.size):
			this_point = self._origin_points[i]
			converted_cord = self._convert_point(this_point[0],this_point[1])
			this_point[0] = converted_cord[0]
			this_point[1] = converted_cord[1]
			if ((this_point[0]>0) & (this_point[1]>0) & (this_point[0]<boundx) & (this_point[1]<boundy)):
				points.append(PointFeatures(this_point,self._map))
		return points

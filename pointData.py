# class for PointFeatures
from utils import *
from geoMap import GeoMap
from sklearn.cluster import DBSCAN

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
		self._rgb = map.get_pixel_value(self._x,self._y)
		self._vector = self._create_features()


	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def rgb(self):
		return self._rgb

	@property
	def Cr(self):
		return self._Cr

	@property
	def vector(self):
		return self._vector

	def _cal_rgb_dis(self,radius=1):
		ref_map = self._map
		value = self._rgb
		total_dis = 0
		for x in range(self._x-radius, self._x+radius+1):
			for y in range(self.y-radius, self._y+radius+1):
				total_dis += eu_distance(ref_map.get_pixel_value(x,y),value)	
		return total_dis

	def _cal_total_std(self,radius=1):
		ref_map = self._map
		matrix = []
		for x in range(self._x-radius, self._x+radius+1):
			for y in range(self.y-radius, self._y+radius+1):
				matrix.append(ref_map.get_pixel_value(x,y))
		return get_std(matrix)

	def _cal_max_min_dis(self,radius=1):
		ref_map = self._map
		dis_list = []
		value = self._rgb
		for x in range(self._x-radius, self._x+radius+1):
			for y in range(self.y-radius, self._y+radius+1):
				if ((x==self._x) & (y==self._y)):
					continue
				else:
					dis_list.append(eu_distance(ref_map.get_pixel_value(x,y),value))
		return [np.max(dis_list),np.min(dis_list)]


	# make sure the radius wont exceed image boundaries	
	def _create_features(self):
		vector = []
		bands = self._rgb
		vector.extend(bands)
		bands_std = get_std(bands)
		vector.append(bands_std)
		rgb_dis = []
		rgb_std = []
		for i in range(1,5):
			rgb_dis.append(self._cal_rgb_dis(i))
		for i in range(1,4):
			rgb_std.append(self._cal_total_std(i))
		vector.extend(rgb_dis)
		vector.append(get_std(rgb_dis))
		vector.extend(rgb_std)
		vector.append(get_std(rgb_std))
		vector.extend(self._cal_max_min_dis())
		return vector



class SampleSet(object):
	def __init__(self, dataPath, mapPath, boundary=None):
		self._map = GeoMap(mapPath)
		self._origin_points = get_sampling_points(dataPath)
		self._size = len(self._origin_points)
		if boundary is None:
			self._bleft = 0
			self._bright = self._map.xsize
			self._bbottom = 0
			self._btop = self._map.ysize
		else:
			self._bleft = boundary[0]
			self._bright = boundary[1]
			self._bbottom = boundary[2]
			self._btop = boundary[3]
			#print(boundary)
		self._featured_points = self._create_points()
		self._rgb_dbscan_labels = self._clustering_DBSCAN()
		self._fsize = len(self._featured_points)

	@property
	def size(self):
		return self._fsize

	@property
	def points(self):
		return self._featured_points

	@property
	def rgb_labels(self):
		return self._rgb_dbscan_labels
	
	
	def _convert_point(self,x,y):
		ref_map = self._map
		x0 = ref_map.x0
		y0 = ref_map.y0
		pw = ref_map.pixel_width
		ph = ref_map.pixel_height
		return int((x-x0)/pw),int((y-y0)/ph)

	def _is_in_boundary(self,x,y):
		l = self._bleft
		r = self._bright
		b = self._bbottom
		t = self._btop
		return ((x>l) & (x<r) & (y>b) & (y<t))

	def _create_points(self):
		points = []
		for i in range(self._size):
			this_point = self._origin_points[i]
			converted_cord = self._convert_point(this_point[0],this_point[1])
			this_point[0] = converted_cord[0]
			this_point[1] = converted_cord[1]
			#print(this_point[0],this_point[1])
			if (self._is_in_boundary(this_point[0],this_point[1])):
				#print(1)
				points.append(PointFeatures(this_point,self._map))
		return points

	def _clustering_DBSCAN(self):
		matrix = [each.rgb for each in self.points]
		# change params here
		clustering_re = DBSCAN(eps=3, min_samples=3).fit(matrix)
		labels = clustering_re.labels_
		return labels















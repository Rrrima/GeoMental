# class for PointFeatures
from utils import *
from geoMap import GeoMap
from sklearn.cluster import DBSCAN
import numpy as np
import math


# get point features for those have metal concentration values
class PointFeatures(object):
	def __init__(self, ct, data, map):
		# data: data in row from xls
		self._map = map
		self._ct = ct
		self._x = data[0]
		self._y = data[1]
		self._pH = data[2]
		self._Cr = data[3]
		self._Pb = data[4]
		self._As = data[5]
		self._rgb = map.get_pixel_value(self._x,self._y)
		self._vector = self._extend_features()
		self._test_content = self._test()


	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def rgb(self):
		return self._rgb
    
    # change the mental element HERE
    # TODO: change it into another representitive way
	@property
	def Cr(self):
		return self._As

	@property
	def pH(self):
		return self._pH
	
	
	@property
	def vector(self):
		return self._vector

	@property
	def test_content(self):
		return self._test_content
	

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

	# 1. mean(mean(r+g+b)) in radius
	# 2. mean(r) in radius
	# 3. mean(g) in radius
	# 4. mean(b) in radius
	# 5. mean(max)
	# 6. mean(min)
	def _cal_mean_rgb(self,radius):
		ref_map = self._map
		rgb_mean = []
		r = []
		g = []
		b = []
		rgb_max = []
		rgb_min = []
		for x in range(self._x-radius, self._x+radius+1):
			for y in range(self.y-radius, self._y+radius+1):
				this_rgb = ref_map.get_pixel_value(x,y)
				rgb_mean.append(np.mean(this_rgb))
				r.append(this_rgb[0])
				g.append(this_rgb[1])
				b.append(this_rgb[2])
				rgb_max.append(max(this_rgb))
				rgb_min.append(min(this_rgb))
		return [np.mean(rgb_mean),np.mean(r),np.mean(g),\
		         np.mean(b),np.mean(rgb_max),np.mean(rgb_min)]

	def _cal_brightness_index(self):
		ref_map = self._map
		x = self._x
		y = self._y
		this_rgb = ref_map.get_pixel_value(x,y)
		bi = sum([math.pow(x,2) for x in this_rgb])/3
		return bi

	def _cal_coloration_index(self):
		ref_map = self._map
		x = self._x
		y = self._y
		this_rgb = ref_map.get_pixel_value(x,y)
		r = this_rgb[0]
		g = this_rgb[1]
		if (r+g==0):
			r = 1
		ci = (r-g)/(r+g)
		return ci

	def _cal_red_index(self):
		ref_map = self._map
		x = self._x
		y = self._y
		this_rgb = ref_map.get_pixel_value(x,y)
		r = this_rgb[0]
		g = this_rgb[1]
		b = this_rgb[2]
		if b==0:
			b=1
		if g==0:
			g=1
		ri = (r/b) * (r/g)
		return ri

	def _cal_fe_index(self):
		ref_map = self._map
		x = self._x
		y = self._y
		this_rgb = ref_map.get_pixel_value(x,y)
		r = this_rgb[0]
		g = this_rgb[1]
		fi = r/g
		return fi

	# make sure the radius wont exceed image boundaries	
	def _create_features(self):
		vector = []
		bands = self._rgb
		vector.extend(bands)
		bands_std = get_std(bands)
		vector.append(bands_std)
		
		rgb_dis = []
		rgb_std = []
		bmax = self._ct.bmax
		bmin = self._ct.bmin
		stp = self._ct.step

		for i in range(bmin,bmax,stp):
			rgb_dis.append(self._cal_rgb_dis(i))
		for i in range(bmin,bmax,stp):
			rgb_std.append(self._cal_total_std(i))
		vector.extend(rgb_dis)
		vector.append(get_std(rgb_dis))
		vector.extend(rgb_std)
		vector.append(get_std(rgb_std))
		vector.extend(self._cal_max_min_dis())
		for i in range(bmin,bmax,stp):
			vector.extend(self._cal_mean_rgb(i))
		
		vector.append(self._cal_brightness_index())
		vector.append(self._cal_coloration_index())
		vector.append(self._cal_red_index())
		vector.append(self._cal_fe_index())
		
		print("******",bands,"******")
		print (vector)
		return vector

	def _extend_features(self):
		vector = []
		this_rgb = self._rgb
		r = this_rgb[0]
		g = this_rgb[1]
		b = this_rgb[2]
		if r==0:
			r=1
		if g==0:
			g=1
		if b==0:
			b=1
		vector.extend([r/b,g/r,g/b,b/r,b/g])
		vector.extend([b/r*(b/g),g/r*(g/b)])
		vector.extend([(r-b)/(r+b),(g-b)/(g+b)])
		print("******",this_rgb,"******")
		print (vector)
		return vector

	def _test(self):
		vector = []
		bands = self._rgb
		print("******",bands,"******")
		"""
		vector.extend(bands)
		vector.append(self._cal_brightness_index())
		vector.append(self._cal_coloration_index())
		vector.append(self._cal_red_index())
		vector.append(self._cal_fe_index())
		"""
		return vector
	# attr should be an array []
	def extend_vector(self,attr):
		self.vector.extend(attr)




class SampleSet(object):
	def __init__(self, ct, dataPath, mapPath, boundary=None):
		self._map = GeoMap(mapPath)
		self._origin_points = get_sampling_points(dataPath)
		self._size = len(self._origin_points)
		self._ct = ct
		self._sh = ct.sh
		self._sv = ct.sv
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
		# self._rgb_dbscan_labels = self._clustering_DBSCAN()
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
			this_point[0] = converted_cord[0]+self._sh
			this_point[1] = converted_cord[1]+self._sv
			#print(this_point[0],this_point[1])
			if (self._is_in_boundary(this_point[0],this_point[1])):
				#print(1)
				this_ptf = PointFeatures(self._ct, this_point, self._map)
				points.append(this_ptf)
				#print(this_ptf.vector)
		return points
   
	def _clustering_DBSCAN(self):
		matrix = [each.rgb for each in self.points]
		# change params here
		clustering_re = DBSCAN(eps=3, min_samples=3).fit(matrix)
		labels = clustering_re.labels_
		return labels
	

	

















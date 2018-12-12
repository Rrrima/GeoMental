from osgeo import gdal

gdal.AllRegister()

# map features
class MapFeatures(object):
	def __init__(self,path):
		self._data = gdal.Open(path)
		data
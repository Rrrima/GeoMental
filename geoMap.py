from osgeo import gdal

gdal.AllRegister()

# geo map features
class GeoMap(object):
	def __init__(self,path):
		self._data = gdal.Open(path)
		data = self._data
		self._adf = data.GetGeoTransform()
		self._rx = self._adf[2]
		self._ry = self._adf[4]
		self._x0 = self._adf[0]
		self._y0 = self._adf[3]
		self._pw = self._adf[1]
		self._ph = self._adf[5]
		self._nX = data.RasterXSize
		self._nY = data.RasterYSize
		self._nB = data.RasterCount

	@property
	def x0(self):
		return self._x0

	@property
	def y0(self):
		return self._y0
	
	@property
	def pixel_width(self):
		return self._pw

	@property
	def pixel_height(self):
		return self._ph

	# TODO: check if x,y are in the right sequence
	def get_pixel_value(self, x, y, bands_id=None):
		if bands_id is None:
			bands_id = range(self._nB)
		pvalues = []
		data = self._data
		for band_id in bands_id:
			band = data.GetRasterBand(band_id+1)
			pvalues.append(band.ReadAsArray(x,y,1,1)[0][0])
		return pvalues

	
	

	
from joblib import load
from sklearn.neural_network import MLPRegressor
from utils import *
from os import walk,path
from name_generator import generate_names
from pointData import PointFeatures, SampleSet
import numpy as np
from geoMap import GeoMap
import matplotlib.pyplot as plt
from cvinfo import *

"""
def test_single_model(matrix,modelPath):
	nn_model = load(modelPath)
	py = nn_model.predict(matrix)
	return py

def test_model_in_file(matrix,rootPath):
	pys = []
	names = []
	for r,d,f in walk(rootPath):
		for name in f:
			modelPath = path.join(rootPath,name)
			if '.joblib' in modelPath:
				py = test_single_model(matrix,modelPath)
				name = name.replace('.joblib','')
				pys.append(py)
				names.append(name)
	return pys,names

"""

FILEPATH_SAMPLE = 'data/top_data.xls'
FILEPATH_FACCV = 'data/cv_info.xlsx'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'
BOUNDARY_TR = [8000,13400,3800,5850]
BOUNDARY_TEST = [3500,6500,1000,3000]
BOUNDARY_TEST2 = [3500,6500,2000,5000]
BOUNDARY_ALL = [3500,13400,1000,9000]


CTN = C(0,0,3,30,40)

FACTORY = [[5458,2981],[4917,3128],[10397,5153],
			[10154,5482],[8766,6525]]
RIVER = [[4237,3508],[7124,5614],[7782,5178],
		[8436,4599],[9121,4227],[9952,4144],
		[10852,4200],[12426,4391]]
GREEN = [[12219,5199],[8766,6524],[4807,1702]]

def get_test_content():
	ATT_NAMES = generate_names()
	print("genrating names")
	print(ATT_NAMES)
	print("preparing sets")
	my_set = SampleSet(CTN, FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY_ALL)

def get_points():
	my_set = SampleSet(CTN, FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY_ALL)
	points = my_set.points
	for pt in points:
		print(pt.rgb,pt.x,pt.y)

def draw_all_map():
	m = GeoMap(FILEPATH_MAP)
	nx = m.xsize
	ny = m.ysize
	pw = m.pixel_width
	ph = m.pixel_height
	xlist = []
	ylist = []
	clist = []
	for i in range(3500,13400,20):
		for j in range(1000,9000,20):
			#print(i,j)
			xlist.append(i)
			ylist.append(j)
			cmap = m.get_pixel_value(i,j)
			clist.append([x/255.0 for x in cmap])
	print(clist,xlist,ylist)
	
	fig = plt.figure()
	plt.scatter(xlist,ylist,c=clist,alpha=0.5)

	plt.scatter(get_xcord(FACTORY),get_ycord(FACTORY),c='crimson', alpha=0.9,marker ='^')
	plt.scatter(get_xcord(RIVER),get_ycord(RIVER),c='yellow', alpha=0.9,marker ='^')
	plt.scatter(get_xcord(GREEN),get_ycord(GREEN),c='white', alpha=0.9,marker ='^')
	my_set = SampleSet(CTN, FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY_ALL)
	show_concentration(my_set.points)
	plt.show()
	



if __name__ == "__main__":
	draw_coarse()
	#my_set = SampleSet(CTN, FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY_ALL)
	#add_cv_attr(my_set)
	#show_map(my_set)

	"""
	points = points = my_set.points
	xmin = min([pt.x for pt in points])
	xmax = max([pt.x for pt in points])
	ymin = min([pt.y for pt in points])
	ymax = max([pt.y for pt in points])
	concent_map = prepare_concent_map(points)
	#print(concent_map)
	"""
	#show_concentration(my_set.points)
	#draw_all_map()
	#data = get_all_cv_items(FILEPATH_FACCV)
	#print(data)
	#add_cv_attr(my_set)
	














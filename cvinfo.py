# define the points for different places
from utils import eu_distance
from collections import defaultdict
import pandas as pd 
import math
import matplotlib.pyplot as plt

FACTORY = [[8821,6559],[9679,6112],[9849,5169],
			[10496,5169],[10526,5609],[10625,4991],[8856,5325],
			[5816,3281],[5279,3544],[6219,3090],
			[6872,4034],[6837,4864],[6096,4367]]
RIVER = [[5110,7695],[6061,6957],[8553,4480],
		[6580,5871],[7543,5034],[9446,4183],
		[11588,4317],[13245,4402],[12329,5325]]
GREEN = [[10100,7929],[12615,7539],[3662,2629],
		[5769,4906],[3610,5077]]

cvs = ['FACTORY','RIVER','GREEN']
CVINFO_ITEMS = ['CF','SD','LZ','WR']
FILEPATH_FACCV = 'data/cv_info.xlsx'

def draw_coarse():
	fx = [each[0] for each in FACTORY]
	fy = [each[1] for each in FACTORY]
	rx = [each[0] for each in RIVER]
	ry = [each[1] for each in RIVER]
	gx = [each[0] for each in GREEN]
	gy = [each[1] for each in GREEN]
	plt.scatter(fx, fy, color = 'orange', alpha=1, marker = '*',s=100)
	plt.scatter(rx, ry, color = 'lightskyblue', alpha=1, marker = '*',s=100)
	plt.scatter(gx, gy, color = 'yellowgreen', alpha=1, marker = '*',s=100)
	plt.show()


def get_all_cv_items(path):
	data = pd.read_excel(path, index_col=None).values
	#print(data)
	cv_items = defaultdict(list)
	for each in data:	
		cv_items[each[0]].append([each[1],each[2]])
	return cv_items


def find_min(point, target,items_dict=None):
	if target=='FACTORY':
		t = FACTORY
	elif target == 'RIVER':
		t = RIVER
	elif target == 'GREEN':
		t = GREEN
	else:
		t = items_dict[target]

	x = point.x
	y = point.y
	min_dis = min([eu_distance(cur,[x,y]) for cur in t])
	return min_dis

def find_deriv(point, target,items_dict=None):
	if target=='FACTORY':
		t = FACTORY
	elif target == 'RIVER':
		t = RIVER
	elif target == 'GREEN':
		t = GREEN
	else:
		t = items_dict[target]	
	x = point.x
	y = point.y
	min_dis = eu_distance(t[0],[x,y])
	min_cord = t[0]
	for cur in t:
		cur_dis = eu_distance(cur,[x,y])
		if (cur_dis < min_dis):
			min_cord = cur
	dx = min_cord[0] - x
	dy = min_cord[1] - y
	lenth = math.sqrt(math.pow(dx,2)+math.pow(dy,2))
	if lenth==0:
		return [0,0]
	else:
		return [dx/lenth,dy/lenth]


def add_cv_attr(sampleset):
	points = sampleset.points
	items_dict = get_all_cv_items(FILEPATH_FACCV)
	for eachpt in points:
		attr = []
		for target in cvs:
			attr.append(find_min(eachpt,target))
		for target in CVINFO_ITEMS:
			attr.append(find_min(eachpt,target,items_dict=items_dict))
		print(attr)
		eachpt.extend_vector(attr)
		print("success add min distance!")
	for eachpt in points:
		attr = []
		for target in cvs:
			attr.extend(find_deriv(eachpt,target))
		for target in CVINFO_ITEMS:
			attr.extend(find_deriv(eachpt,target,items_dict=items_dict))
		print(attr)
		eachpt.extend_vector(attr)
		print("success add derivatives!")






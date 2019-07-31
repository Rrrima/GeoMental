import xlrd
import pprint
import numpy as np 
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import xlwt
from decimal import *
from scipy.stats.stats import pearsonr 
import collections
import seaborn as sns

pp = pprint.PrettyPrinter(indent=4)
# x:latitude
# y:longtitude
CRI = {
	'As':[[30,200],[30,150],[25,120],[20,100]],
	'Pb':[70,90,120,170],
	'Cr':[150,150,200,250]
}

#define important constant
class C(object):
	def __init__(self,sh=0,sv=0,step=3,bb=30,bt=37):
		self._sh = sh
		self._sv = sv
		self._step = step
		self._bmin = bb
		self._bmax = bt
	@property
	def sh(self):
		return self._sh

	@property
	def sv(self):
		return self._sv

	@property
	def step(self):
		return self._step

	@property
	def bmax(self):
		return self._bmax

	@property
	def bmin(self):
		return self._bmin
	
		
def zo_scale(arr,scaleSize=None):
	if scaleSize is None:
		vmin = np.min(arr)
		vmax = np.max(arr)
	else:
		vmin = scaleSize[0]
		vmax = scaleSize[1]
	return [(x-vmin)/(vmax-vmin) for x in arr]

def get_sampling_points(filePath):
	data = []
	book = xlrd.open_workbook(filePath)
	table = book.sheets()[0]
	nrows = table.nrows
	for i in range(1,nrows):
		data.append(table.row_values(i))
	return data

def get_std(arr):
	return np.std(arr)

def eu_distance(a,b):
	return distance.euclidean(a, b)

def find_max(arr):
	arr = np.array(arr)
	arr.flatten()
	return np.max(arr)

def find_min(arr):
	arr = np.array(arr)
	arr.flatten()
	return np.min(arr)


def pre_training_set(data,size=None,constrain=None):
	xlist = []
	ylist = []
	matrix = []
	target = []
	tph = []
	if size is None:
		size = len(data)
	if constrain is None:
		for i in range(size):
			ty = data[i].Cr
			if ty!='':
				xlist.append(data[i].x)
				ylist.append(data[i].y)
				matrix.append(data[i].vector)
				target.append(data[i].Cr)
				tph.append(data[i].pH)
	else:
		vmin = constrain[0]
		vmax = constrain[1]
		for i in range(size):
			ty = data[i].Cr
			if  ty!='':
				if (ty>=vmin)&(ty<=vmax):
					xlist.append(data[i].x)
					ylist.append(data[i].y)
					matrix.append(data[i].vector)
					target.append(data[i].Cr)
					tph.append(data[i].pH)

	return xlist,ylist,matrix,target,tph

def print_rgb_map(data):
	xlist = [data.x for data in my_data]
	ylist = [data.y for data in my_data]
	clist = [tuple([x/255 for x in data.rgb]) for data in my_data]
	plt.scatter(xlist, ylist, c=clist, alpha = 0.6)
	plt.show()

def print_mental_map(xlist,ylist,mental):
	plt.scatter(xlist, ylist, c=zo_scale(mental), alpha = 0.8)
	plt.show()

def find_by_value(points, vmin, vmax):
	cord_set = []
	for point in points:
		if (point.Cr>=vmin) & (point.Cr<=vmax):
			cord_set.append([point.x,point.y])
	return cord_set

def remove_by_value(xlist,ylist,vmin,vmax,pv):
	n_xl = []
	n_yl = []
	n_p = []
	for i in range(len(pv)):
		if not ((pv[i]>vmin)&(pv[i]<vmax)):
			n_p.append(pv[i])
			n_xl.append(xlist[i])
			x_yl.append(ylist[i])
	return n_xl,n_yl,n_p

def print_compared_mental_map(xlist,ylist,ty,py):
	fig, axs = plt.subplots(1, 2)
	fig.suptitle('models training vs prediction')
	vmin = np.min([np.min(ty),np.min(py)])
	vmax = np.max([np.max(ty),np.max(py)])
	print(py)
	clist = [zo_scale(ty,[vmin,vmax]),zo_scale(py,[vmin,vmax])]
	print(clist[1])
	images = []
	for j in range(2):
		images.append(axs[j].scatter(xlist,ylist,c=clist[j]))
		axs[j].label_outer()
	fig.colorbar(images[0], ax=axs, orientation='horizontal', fraction=.1)
	plt.show()

def print_all_mental_maps(xlist,ylist,mental_values,names):
	num = len(mental_values)
	nr = int((num-1)/3)
	vmin = find_min(mental_values)
	vmax = find_max(mental_values)
	clist = []
	images = []
	for mv in mental_values:
		clist.append(zo_scale(mv,[vmin,vmax]))
	if nr>0:
		fig, axs = plt.subplots(nr+1,3)
		fig.suptitle('overall models',fontsize=14, fontweight='bold')
		for i in range(nr+1):
			for j in range(3):
				if (3*i+j)<num:
					images.append(axs[i,j].scatter(xlist,ylist,c=clist[3*i+j],s=8))
					axs[i,j].set_title(names[3*i+j],fontsize=5)
					axs[i,j].label_outer()
	if nr==0:
		fig, axs = plt.subplots(1,num)
		fig.suptitle('overall models',fontsize=14, fontweight='bold')
		for j in range(num):
			images.append(axs[j].scatter(xlist,ylist,c=clist[j],s=8))
			axs[j].set_title(names[j],fontsize=5)
			axs[j].label_outer()
	fig.colorbar(images[0], ax=axs, orientation='horizontal',fraction=.05)
	plt.show()

def dump_to_excel_predictions(names,pys):
	workbook = xlwt.Workbook(encoding = 'utf-8')
	worksheet = workbook.add_sheet('results_nn_test')
	for i in range(len(names)):
		worksheet.write(0,i, names[i])
	for i in range(len(pys)):
		py = pys[i]
		for j in range(len(py)):
			worksheet.write(j+1,i, py[j])
	workbook.save('prediction_results.xls')

def dump_to_excel_attributes(lx,ly,names,matrix,results,out_name):
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet('attri_results')
	worksheet.write(0,0,'latitude')
	worksheet.write(0,1,'longtitude')
	for i in range(len(lx)):
		worksheet.write(i+1,0,lx[i])
	for i in range(len(ly)):
		worksheet.write(i+1,1,ly[i])
	print("finish dumping coordinate")
	workbook.save(out_name)
	for i in range (len(names)):
		worksheet.write(0,i+2,names[i])
	worksheet.write(0,len(names)+2,'mental')
	print("finish dumping names")
	workbook.save(out_name)
	for i in range(len(matrix)):
		point_v = matrix[i]
		print(point_v)
		for j in range(len(point_v)):
			worksheet.write(i+1,j+2,Decimal(str(round(point_v[j],3))))
	print("finish dumping vecotrs")
	workbook.save(out_name)
	for i in range(len(results)):
		worksheet.write(i+1,len(names)+2,results[i])
	print("finish dumping results")
	workbook.save(out_name)
    # calculate pearson cor-relationship and p-value
	num_records = len(matrix)
	for i in range(len(names)):
		attri = []
		for j in range(num_records):
			attri.append(matrix[j][i])
		r,p = pearsonr(attri,results)
		worksheet.write(num_records+1,i+2,r)
		worksheet.write(num_records+2,i+2,p)
	print("finish pearson analysis")
	workbook.save(out_name)
	worksheet.write(num_records+1,0,'pearson_corr')
	worksheet.write(num_records+2,0,'p_value')

	workbook.save(out_name)


def show_map(sampleset):
	my_set = sampleset
	points = my_set.points
	# Create plot
	fig = plt.figure()
	for pt in points:
		cmap = [x/255.0 for x in pt.rgb]
		plt.scatter(pt.x, pt.y, c=cmap, alpha=0.5)
		print(pt.x,pt.y,cmap)
	plt.show()


def prepare_concent_map(points):
	matrix_map = collections.defaultdict(lambda: collections.defaultdict(int))
	for pt in points:
		if pt.Cr != '':
			matrix_map[pt.x][pt.y] = pt.Cr
	xlist = [xx for xx in set([pt.x for pt in points])]
	ylist = [xx for xx in set([pt.y for pt in points])]
	xlist.sort()
	ylist.sort()
	mymap = pd.DataFrame(index=xlist,columns=ylist)
	
	for x in xlist:
		for y in ylist:
			print(x,y)
			v = int(matrix_map[x][y])
			mymap.set_value(x,y,v)
	return mymap



def show_concentration(data):
	points = data
	xlist = [pt.x for pt in points]
	ylist = [pt.y for pt in points]
	clist = []
	criteria = [15,30,300]
	for pt in points:
		v = pt.Cr
		if v!= '':
			if v<=criteria[0]:
				clist.append('lightskyblue')
			elif v<=criteria[1]:
				clist.append('orange')
			elif v<=criteria[2]:
				clist.append('plum')
			elif v>criteria[2]:
				clist.append('crimson')
		if v=='':
			clist.append('white')
	plt.scatter(xlist, ylist, c=clist, alpha=0.2,)
	plt.show()
	print(c)

def show_this_map(corx,cory,lty):
	clist = []
	for each in lty:
		if each==2:
			clist.append('crimson')
		elif each==1:
			clist.append('orange')
		elif each==0:
			clist.append('lightskyblue')
	plt.scatter(corx, cory, c=clist, alpha=0.4,)
	plt.show()

def save_this_map(corx,cory,lty,lty2,sp):
	fig, axes = plt.subplots(nrows=2, ncols=1)
	clist = []
	clist2 = []
	for each in lty:
		if each==2:
			clist.append('crimson')
		elif each==1:
			clist.append('orange')
		elif each==0:
			clist.append('lightskyblue')
	for each in lty2:
		if each==2:
			clist2.append('crimson')
		elif each==1:
			clist2.append('orange')
		elif each==0:
			clist2.append('lightskyblue')
	axes[0].scatter(corx, cory, c=clist, alpha=0.65)
	axes[1].scatter(corx, cory, c=clist2, alpha=0.65)
	fig.set_size_inches(5, 6)
	plt.savefig(sp)



def get_logistic_value(ty,tph,metal):
	criteria = CRI[metal]
	clist = []
	for i in range(len(ty)):
		ph = tph[i]
		y = ty[i]
		if ph<=5.5:
			if y<=criteria[0][0]:
				clist.append(0)
			elif y<=criteria[0][1]:
				clist.append(1)
			else:
				clist.append(2)
		elif ph<=6.5:
			if y<=criteria[1][0]:
				clist.append(0)
			elif y<=criteria[1][1]:
				clist.append(1)
			else:
				clist.append(2)
		elif ph<=7.5:
			if y<=criteria[2][0]:
				clist.append(0)
			elif y<=criteria[2][1]:
				clist.append(1)
			else:
				clist.append(2)
		else:
			if y<=criteria[3][0]:
				clist.append(0)
			elif y<=criteria[3][1]:
				clist.append(1)
			else:
				clist.append(2)
	return clist

def get_xcord(list):
	return [each[0] for each in list]

def get_ycord(list):
	return [each[1] for  each in list]














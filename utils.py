import xlrd
import pprint
import numpy as np 
from scipy.spatial import distance
import matplotlib.pyplot as plt
import xlwt

pp = pprint.PrettyPrinter(indent=4)
# x:latitude
# y:longtitude
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

	return xlist,ylist,matrix,target

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

def dump_to_excel(names,pys):
	workbook = xlwt.Workbook(encoding = 'utf-8')
	worksheet = workbook.add_sheet('results_nn_test')
	for i in range(len(names)):
		worksheet.write(0,i, names[i])
	for i in range(len(pys)):
		py = pys[i]
		for j in range(len(py)):
			worksheet.write(j+1,i, py[j])
	workbook.save('results_nn_test_as.xls')














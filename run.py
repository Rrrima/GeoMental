#from test import *
from train import *
from utils import *
from pointData import PointFeatures, SampleSet
import numpy as np
from name_generator import generate_names,re_generate_names
from analysis import *
import time
from cvinfo import *
import pandas as pd
import os
from collections import defaultdict

FILEPATH_SAMPLE = 'data/top_data.xls'
# USE ABSOLUTE PATH!
FILEPATH_MAP = '/Users/rima/GeoMental/zx_field_data/map.tif'
ROOT_PATH = 'nn_models/apr_6'
BOUNDARY_TR3 = [8000,13400,3800,5850]
BOUNDARY_TR4 = [3500,6500,5000,9000]
BOUNDARY_TR1 = [3500,6500,1000,3000]
BOUNDARY_TR2 = [3500,6500,2000,5000]
BOUNDARY_ALL = [3500,13400,1000,5850]
# outname: metal_sampleset_ctn_timestamp
NAME = 'ALL'
#(self,sh=0,sv=0,step=3,bb=30,bt=37)
CTN = C(0,0,5,0,60)

def get_training_set(path):
	data = pd.read_excel(path).values
	matrix = []
	ty = []
	for each in data:
		if '_' not in str(each[0]):
			matrix.append([each[i] for i in range(0,len(each)-1)])
			ty.append(each[-1])
	return matrix,ty
 

def create_vector():
	print("preparing data points")
	my_set = SampleSet(CTN, FILEPATH_SAMPLE, FILEPATH_MAP, BOUNDARY_ALL)
	#add_cv_attr(my_set)
	my_data = my_set.points
	print("preparing vectors")
	xlist,ylist,matrix,ty,tph = pre_training_set(my_data)
	logistic_ty = get_logistic_value(ty,tph,'As')
	ATT_NAMES = re_generate_names()
	#num_att = len(matrix[0])
	timestamp = str(int(time.time()))
	OUT_NAME = NAME + '_'+timestamp + '.xls'
	print("genrating names")
	print(ATT_NAMES)
	print("dumping to excel as:",OUT_NAME)
	dump_to_excel_attributes(xlist,ylist,ATT_NAMES,matrix,logistic_ty,OUT_NAME)
	show_this_map(xlist,ylist,logistic_ty)


def analysis_vector():
	ATT_NAMES = generate_names()
	size_trend_analysis(OUT_NAME,ATT_NAMES)

def create_folders(alg):
	os.makedirs(alg)
	for i in range(5,96,5):
		os.makedirs(alg+'/'+str(i))

def analysis_result(origin_y,predict_y):
	tt = 0
	fb = 0
	fs = 0
	for i in range(len(origin_y)):
		x = origin_y[i]
		y = predict_y[i]
		if x==y :
			tt+=1
		elif x<y:
			fb+=1
		elif x>y:
			fs+=1
	tot = tt+fb+fs
	return [tt/tot,fb/tot,fs/tot]

def run_alg_analysis(matrix,ty,ALG):
	all_score = defaultdict(list)
	for i in range(5,96,5):
		scores = []
		for j in range(10):
			#PATH = ALG+'/'+ str(i) + '/' + str(j)
			data,tt = train_extra_forest(matrix,ty,i)
			#output = pd.DataFrame(data)
			#trainingset = pd.DataFrame(tt)
			#output.to_excel(PATH+'_P.xls')
			#trainingset.to_excel(PATH+'_T.xls')
			#save_this_map(data['xcord'],data['ycord'],data['origin_y'],data['predict_y'],PATH+'.png')
			result = analysis_result(data['origin_y'],data['predict_y'])
			scores.append(result)
		print(scores)
		allre = pd.DataFrame(scores)
		#allre.to_excel(ALG+'/'+ str(i) + '/'+'scores.xls')
		all_score[str(i)+'_accuracy'] = [score[0] for score in scores]
		all_score[str(i)+'_FP'] = [score[1] for score in scores]
		all_score[str(i)+'_FN'] = [score[2] for score in scores]
	output_scores = pd.DataFrame(all_score)
	output_scores.to_excel(ALG+'_scores.xls')




if __name__ == "__main__":
	# pys,names = test_model_in_file(matrix,ROOT_PATH)
	# print(ty,py)
	# print_compared_mental_map(xlist,ylist,ty,py)
	# pys.append(ty)
	# names.append('training_set')
	# print_all_mental_maps(xlist,ylist,pys,names)
	# create_vector()
	# analysis_vector()
	ALG = 'EF_gini'
	#create_folders(ALG)
	matrix,ty = get_training_set('data/all.xlsx')
	print(matrix,ty)
	#corrx = np.round(np.corrcoef(matrix), 2)
	#output = pd.DataFrame(corrx)
	#print(output)
	#output.to_csv('cor_for_matrix.csv')

	#train_plsr(matrix,ty,15)
	#data,tt,prob = train_svm(matrix,ty,20)
	#output = pd.DataFrame(data)
	#matrix = prob
	#ty = data['origin_y']
	run_alg_analysis(matrix,ty,ALG)
	#print(matrix,ty)
	# result = pd.DataFrame(predict_result)
	# timestamp = str(int(time.time()))	
	# OUT_NAME = 'ef' +timestamp+ '.xls'
	#output.to_excel(OUT_NAME)

	
		

















	
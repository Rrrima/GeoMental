# test classes 
# REMOVE it from the final project
import pprint
import numpy as np
import matplotlib.pyplot as plt
from joblib import dump
from os import path
from sklearn.neural_network import MLPRegressor
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.cross_decomposition import PLSRegression

np.set_printoptions(threshold=np.inf)
pp = pprint.PrettyPrinter(indent=4)
from utils import *

#### neural network model ####
def train_nn_model(matrix,ty):
	# train using nn
	params_dict = defaultdict(int)
	for hls in [10]:
		for alp in [0.0001]:
			for mi in [2000]:
				best_index = 0
				min_loss = 99999999
				current_index = 0
				while(current_index<1000):
					nn_result = MLPRegressor(hidden_layer_sizes=hls, alpha =alp, max_iter=mi).fit(matrix,ty)
					print(nn_result.loss_)
					if min_loss>nn_result.loss_:
						best_index = current_index
						min_loss = nn_result.loss_
						best_model = nn_result
					current_index += 1
				print(min_loss)
				this_key = str(hls)+'-'+str(alp)+'-'+str(mi)
				params_dict[this_key] = min_loss
				dump(best_model, path.join('nn_models','removed2',this_key+'-'+str(int(min_loss))+'.joblib')) 
	print (params_dict)
	

#### random forest model ##
def train_random_forest(matrix,ty,n):
	clf = RandomForestClassifier(n_estimators=10,criterion='entropy',max_features='log2')  
	X_train, X_test, y_train, y_test = train_test_split(matrix, ty, test_size=n/100) 
	clf.fit(X_train, y_train) 
	print_forest_importance(clf,X_train)
	predict_y = clf.predict(X_test)  
	xx = [each[0] for each in X_test]
	yy = [each[1] for each in X_test]
	ox = [each[0] for each in X_train]
	oy = [each[1] for each in X_train]
	return({
		'xcord':xx,
		'ycord':yy,
		'origin_y':y_test,
		'predict_y':predict_y
		},
		{
		'xcord':ox,
		'ycord':oy,
		'y':y_train,
		})  

def train_extra_forest(matrix,ty,n):
	clf = ExtraTreesClassifier(n_estimators=10,criterion='gini', max_depth=None)  
	X_train, X_test, y_train, y_test = train_test_split(matrix, ty, test_size=n/100)  
	clf.fit(X_train, y_train) 
	#print_forest_importance(clf,X_train)
	predict_y = clf.predict(X_test)
	xx = [each[0] for each in X_test]
	yy = [each[1] for each in X_test]
	ox = [each[0] for each in X_train]
	oy = [each[1] for each in X_train]
	return({
		'xcord':xx,
		'ycord':yy,
		'origin_y':y_test,
		'predict_y':predict_y
		},
		{
		'xcord':ox,
		'ycord':oy,
		'y':y_train,
		})  

def print_forest_importance(forest,X):
	X = np.array(X)
	importance_matrix=[]
	importances = forest.feature_importances_
	#print(importances,X)
	std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
	indices = np.argsort(importances)[::-1]
	# Print the feature ranking
	print("Feature ranking:")
	for f in range(X.shape[1]):
		print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
		importance_matrix.append([indices[f], importances[indices[f]]])
	output = pd.DataFrame(importance_matrix)
	output.to_excel('rfentropy.xls')

   


def train_svm(matrix,ty,n):
	clf = SVC(gamma='auto',kernel='rbf',probability=True)
	X_train, X_test, y_train, y_test = train_test_split(matrix, ty, test_size=n/100)
	clf.fit(X_train, y_train) 
	predict_y = clf.predict(X_test)
	prob = clf.predict_proba(X_test)
	print(prob)
	print("y=")
	print(y_test)
	predict_result = [each[1] for each in prob]
	xx = [each[0] for each in X_test]
	yy = [each[1] for each in X_test]
	ox = [each[0] for each in X_train]
	oy = [each[1] for each in X_train]
	return({
		'xcord':xx,
		'ycord':yy,
		'origin_y':y_test,
		'predict_y':predict_y
		},
		{
		'xcord':ox,
		'ycord':oy,
		'y':y_train,
		},
		prob)    

def train_mlp(matrix,ty,n):
	clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(2,))
	clf.fit(matrix, ty)
	X_train, X_test, y_train, y_test = train_test_split(matrix, ty, test_size=n/10)
	scores = cross_val_score(clf, matrix, ty, cv =10)
	predict_result = clf.predict(X_test)
	return(scores,predict_result)  

def train_plsr(matrix,ty,n):
	clf = PLSRegression(n_components=5)
	clf.fit(matrix, ty)
	X_train, X_test, y_train, y_test = train_test_split(matrix, ty, test_size=n/100)
	#scores = cross_val_score(clf, matrix, ty, cv =10)
	scores = clf.score(X_train,y_train)
	print_plsr_importance(clf)
	predict_result = {'predict':[each[0] for each in clf.predict(X_test)],'real':y_test}
	return(scores,predict_result)  

def print_plsr_importance(clf):
	weights = pd.DataFrame(clf.x_weights_)
	loadings =  pd.DataFrame(clf.x_loadings_)
	scores =  pd.DataFrame(clf.x_scores_)

	weights.to_excel('plsr_weights.xls')
	loadings.to_excel('plsr_loadings.xls')
	scores.to_excel('plsr_scores.xls')



	

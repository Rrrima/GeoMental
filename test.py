from joblib import load
from sklearn.neural_network import MLPRegressor
from utils import *
from os import walk,path

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






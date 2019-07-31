from sklearn.decomposition import PCA 
from sklearn.preprocessing import StandardScaler 
from sklearn import linear_model 
from sklearn.model_selection import cross_val_predict 
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)

def pcr_analysis(filename):
	data = pd.read_excel(filename,index_col=None)
	df = pd.DataFrame(data)
	xmatrix = df.values[:-2].T
	y = xmatrix[-1:][0]
	mx = xmatrix[:-1].T
	pca = PCA()
	Xstd = StandardScaler().fit_transform(mx[:,:])
	#print(pca.explained_variance_ratio_)
	Xreg = pca.fit_transform(Xstd)[:,:6]
	#print(Xreg,y)
	#print("+++++++ components +++++++")
	#print(pca.singular_values_)
	regr = linear_model.LinearRegression() 
	regr.fit(Xreg, y)
	# Calibration
	y_c = regr.predict(Xreg)	 
	# Cross-validation
	y_cv = cross_val_predict(regr, Xreg, y, cv=2)	 
	# Calculate scores for calibration and cross-validation
	score_c = r2_score(y, y_c)
	score_cv = r2_score(y, y_cv)	 
	# Calculate mean square error for calibration and cross validation
	mse_c = mean_squared_error(y, y_c)
	mse_cv = mean_squared_error(y, y_cv)
	print(score_c,score_cv)

	plt.scatter(y,y_c)
	plt.show()

pcr_analysis('results/11_16_11_40.xls')

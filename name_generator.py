# generate names for each attribute
# used when output to excel
import utils
from utils import C
import xlwt
CTN = C(0,0,5,0,60)
B_BOTTOM = CTN.bmin
B_TOP = CTN.bmax
STEP = CTN.step

def generate_names():
	names = ['R','G','B','RGB_STD']
	for i in range(B_BOTTOM,B_TOP,STEP):
		names.append('RGB_DIS_'+str(i))
	names.append('DIS_STD')
	for i in range(B_BOTTOM,B_TOP,STEP):
		names.append('RGB_STD_'+str(i))
	names.append('STD_STD')
	names.append('MAX_DIS')
	names.append('MIN_DIS')
	for i in range(B_BOTTOM,B_TOP,STEP):
		names.append('RGB_MEAN_1_'+str(i))
		names.append('RGB_MEAN_2_'+str(i))
		names.append('RGB_MEAN_3_'+str(i))
		names.append('RGB_MEAN_4_'+str(i))
		names.append('RGB_MEAN_5_'+str(i))
		names.append('RGB_MEAN_6_'+str(i))
	names.append('BI')
	names.append('CI')
	names.append('RI')
	names.append('FeI')
	names.extend(['factory_dis','river_dis','green_dis'])
	names.extend(['CF','SD','LZ','WR'])
	names.extend(['factory_dx','factory_dy','river_dx','river_dy','green_dx','green_dy'])
	names.extend(['CF_dx','CF_dy','SD_dx','SD_dy','LZ_dx','LZ_dy','WR_dx','WR_dy'])


	return names

def re_generate_names():
	names = ['R/B','G/R','G/B','B/R','B/G']
	names.extend(['b2/rg','g2/rb'])
	names.extend(['r-b/r+g','g-b/g+b'])
	return names
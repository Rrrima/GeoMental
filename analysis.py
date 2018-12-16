# use this module for result analysis
import xlrd
from collections import defaultdict
import matplotlib.pyplot as plt

def drawout_results(this_dict):
	all_num = int(len(this_dict)/2)
	nrows = int(all_num/3)+1
	fig, axes = plt.subplots(nrows=nrows, ncols=3)
	num = 0
	for cur_key in this_dict.keys():
		if 'RE_' in cur_key:
			x = cur_key.split('_')
			id_key = '_'.join(['ID',x[1],x[2]])
			axi_x = this_dict[id_key]
			axi_y = this_dict[cur_key]
			cr = int(num/3)
			cn = int(num - 3*cr)
			axes[cr,cn].set_title(cur_key,size=10)
			axes[cr,cn].set_xlabel('pixel range',size=8)
			axes[cr,cn].set_ylabel('p value',size=8)
			axes[cr,cn].tick_params(labelsize = 6)
			for i in range(len(axi_x)):
				if axi_y[i]<0.001:
					axes[cr,cn].scatter(int(axi_x[i]),axi_y[i],c='red',s=3)
				else:
					axes[cr,cn].scatter(int(axi_x[i]),axi_y[i],c='gray',s=3)
			axes[cr,cn].grid(True)
			num += 1
	for i in range(num,all_num+1):
		cr = int(i/3)
		cn = int(i - 3*cr)
		axes[cr,cn].set_visible(False)


	plt.tight_layout()
	plt.show()
			

def size_trend_analysis(filename,names):
	data = xlrd.open_workbook(filename)
	table = data.sheets()[0]  
	nrows = table.nrows
	temp =  table.row_values(nrows-1)
	p_value = temp[2:]
	results = defaultdict(list)
	for i in range(len(names)):
		name = names[i]
		x = name.split('_')
		if 'RGB_STD_' in name:
			results['RE_RGB_STD'].append(p_value[i])
			results['ID_RGB_STD'].append(x[2])	
		elif 'RGB_DIS_' in name:
			results['RE_RGB_DIS'].append(p_value[i])
			x = name.split('_')
			results['ID_RGB_DIS'].append(x[2])	
		elif 'RGB_MEAN_1_' in name:
			results['RE_MEAN_MEAN'].append(p_value[i])
			results['ID_MEAN_MEAN'].append(x[3])
		elif 'RGB_MEAN_2_' in name:
			results['RE_MEAN_R'].append(p_value[i])
			results['ID_MEAN_R'].append(x[3])	
		elif 'RGB_MEAN_3_' in name:
			results['RE_MEAN_G'].append(p_value[i])
			results['ID_MEAN_G'].append(x[3])	
		elif 'RGB_MEAN_4_' in name:
			results['RE_MEAN_B'].append(p_value[i])
			results['ID_MEAN_B'].append(x[3])	
		elif 'RGB_MEAN_5_' in name:
			results['RE_MEAN_MAX'].append(p_value[i])
			results['ID_MEAN_MAX'].append(x[3])		
		elif 'RGB_MEAN_6_' in name:
			results['RE_MEAN_MIN'].append(p_value[i])
			results['ID_MEAN_MIN'].append(x[3])
	#print (results)
	drawout_results(results)





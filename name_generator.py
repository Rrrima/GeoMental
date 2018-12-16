import xlwt

def generate_names():
	names = ['R','G','B','RGB_STD']
	for i in range(1,31,3):
		names.append('RGB_DIS_'+str(i))
	names.append('RGB_STD')
	for i in range(1,31,3):
		names.append('RGB_STD_'+str(i))
	names.append('STD_STD')
	names.append('MAX_DIS')
	names.append('MIN_DIS')
	for i in range(1,31,3):
		names.append('RGB_MEAN_1_'+str(i))
		names.append('RGB_MEAN_2_'+str(i))
		names.append('RGB_MEAN_3_'+str(i))
		names.append('RGB_MEAN_4_'+str(i))
		names.append('RGB_MEAN_5_'+str(i))
		names.append('RGB_MEAN_6_'+str(i))

	return names
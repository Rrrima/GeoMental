import xlrd
import pprint

pp = pprint.PrettyPrinter(indent=4)
# x:latitude
# y:longtitude

def get_sampling_points(filePath):
	data = []
	book = xlrd.open_workbook(filePath)
	table = book.sheets()[0]
	nrows = table.nrows
	for i in range(1,nrows):
		data.append(table.row_values(i))
	return data

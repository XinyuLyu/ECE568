#python3
# -*- coding: utf-8 -*-
"""
Three kinds of indicators and will save picture (png).

"""

from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import json

# StockName: GOOG, AMZN, etc
def ROCIndicator(StockName):
	ti = TechIndicators(key='QBGRPFYFV5WBTTCO', output_format='pandas')
	data, meta_data= ti.get_roc(symbol=StockName, interval='30min', time_period=60, series_type ='close')
	realdata = data.to_json(orient='table')
	print(realdata)

	# json_path = './' + StockName +'ROC.json'
	# with open(json_path, "w") as f:
	# 	json.dump(realdata, f)
	# 	print("Complete...")


	# print(type(data))
	# # print(data)
	# data.plot()

	# plt.title('ROC indicator for '+ StockName+ ' stock (1 min)')
	# fig = plt.gcf()
	# plt.savefig("ROC.pdf")
	# plt.show()	 
	# data.to_csv(StockName+'ROC indicator.csv',index=True,sep=',')  

	print('Success')
	

# StockName: GOOG, AMZN, etc
def OBVIndicator(StockName):
	ti = TechIndicators(key='QBGRPFYFV5WBTTCO', output_format='pandas')
	data, meta_data= ti.get_obv(symbol=StockName, interval='30min')
	realdata = data.to_json(orient='table')
	print(realdata)
	# json_path = './' + StockName +'OBV.json'
	# with open(json_path, "w") as f:
	# 	json.dump(realdata, f)
	# 	print("Complete...")


	# data.plot()

	# plt.title('OBV indicator for '+ StockName+ ' stock (1 min)')
	# fig = plt.gcf()
	# plt.savefig("OBV.pdf")
	# plt.show()	
	# data.to_csv(StockName+'OBV indicator.csv',index=True,sep=',') 

	print('Success')

# StockName: GOOG, AMZN, etc
def MACDIndicator(StockName):
	ti = TechIndicators(key='QBGRPFYFV5WBTTCO', output_format='pandas')
	data, meta_data= ti.get_macd(symbol=StockName, interval='30min', series_type ='close')
	realdata = data.to_json(orient='table')
	print(realdata)

	# data.plot()
# =============================================================================
# 	json_path = './' + StockName +'MACD.json'
# =============================================================================
# =============================================================================
# 	with open(json_path, "w") as f:
# 		json.dump(realdata, f)
# 		print("Complete...")
# =============================================================================

	# plt.title('MACD indicator for '+ StockName+ ' stock (1 min)')
	# fig = plt.gcf()
	# plt.savefig("MACD.pdf")
	# plt.show()	
	# data.to_csv(StockName+'MACD indicator.csv',index=True,sep=',') 

	print('Success')


def main():
	# companyNameList = ["GOOG","AABA","AMZN","OPK","FB","TWTR","NFLX","TSLA","BABA","SPLK"]
	# for com in companyNameList:
	# 	ROCIndicator(com)
	# 	OBVIndicator(com)
	# 	MACDIndicator(com)
	MACDIndicator("SPLK")


if __name__ == '__main__':
	main()

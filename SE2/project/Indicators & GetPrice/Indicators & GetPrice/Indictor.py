#python3
# -*- coding: utf-8 -*-
"""
Three kinds of indicators and will save picture (png).

"""

from alpha_vantage.techindicators import TechIndicators

# StockName: GOOG, AMZN, etc
def ROCIndicator(StockName):
	ti = TechIndicators(key='QBGRPFYFV5WBTTCO', output_format='pandas')
	data, meta_data= ti.get_roc(symbol=StockName, interval='1min', time_period=60, series_type ='close') 
	#data.to_csv(StockName+'ROC indicator.csv',index=True,sep=',')  
    return data.to_json(orient='index')
	#return jsonify(data)

# StockName: GOOG, AMZN, etc
def OBVIndicator(StockName):
	ti = TechIndicators(key='QBGRPFYFV5WBTTCO', output_format='pandas')
	data, meta_data= ti.get_obv(symbol=StockName, interval='1min')
	#data.to_csv(StockName+'OBV indicator.csv',index=True,sep=',') 
    return data.to_json(orient='index')
    #return jsonify(data)
#	print('Success')

# StockName: GOOG, AMZN, etc
def MACDIndicator(StockName):
	ti = TechIndicators(key='QBGRPFYFV5WBTTCO', output_format='pandas')
	data, meta_data= ti.get_macd(symbol=StockName, interval='1min', series_type ='close')
	#data.to_csv(StockName+'MACD indicator.csv',index=True,sep=',') 
    return data.to_json(orient='index')
    #return jsonify(data)
	#print('Success')


def main(CompanyId,indicator):
	# companyNameList = ["GOOG","AABA","AMZN","OPK","FB","TWTR","NFLX","TSLA","BABA","SPLK"]
    if indicator == "ROC":
        ROCIndicator(CompanyId)
    if indicator == "OBV":
        OBVIndicator(CompanyId)
    if indicator == "MACD":
    	MACDIndicator('GOOG')


if __name__ == '__main__':
	main()

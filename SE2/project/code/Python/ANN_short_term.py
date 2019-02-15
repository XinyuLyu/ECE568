# -*- coding: utf-8 -*-
"""
# written by: Xinwei Zhao
# assisted by: ZE LIU
# debugged by: All members
"""

# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Dropout
#from keras.optimizers import Adam
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
import numpy
import csv
import json

# def load_dataset(path):
#     with open(path,"r") as csvfile:
#         reader = csv.DictReader(csvfile)
#         dataset = [row['Close'].replace(',','') for row in reader]
#     dataset = [float(i) for i in dataset ]
#     return dataset
def ANNPredict(StockName):
	engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/TESTDB')
	df = pd.read_sql_query('SELECT * FROM '+StockName+'_History_Price', engine)
	newData = df.values.T.tolist()

	# newData is a big list of the history price and we only need close price now
	ClosePrice = newData[4]
	for i in range(0, len(ClosePrice)):
		ClosePrice[i] = float(ClosePrice[i])

	dataset = ClosePrice
	# print(dataset)
	# print(type(dataset))
	seed = 7
	numpy.random.seed(seed)
	data = numpy.array(dataset)
	# 100 / 5 =20
	data = data.reshape((-1, 20))
	#print(data)

	X = data[:4, 0:19]
	Y = data[:4, 19]
	Test_X = data[4:, 0:19]
	Test_Y = data[4:, 19]
	Prediction = data[4:,1:19]


	'''
	print(X)
	print(Y)
	print(Test_X)
	print(Test_Y)
	print(Prediction)
	'''
	model = Sequential()
	#model.add(Dense(30, input_shape=(35,), activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None))
	model.add(Dense(30, input_shape=(19,), activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None))
	model.add(Dense(17, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None))
	model.add(Dense(3, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None))
	model.add(Dense(1, activation=None, use_bias=None, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None))
	model.compile(loss='mse',optimizer='adam')
	model.fit(X, Y, epochs=500, batch_size=20, verbose = 0)
	# verbose means do not display the process of training

	Result = model.predict(Test_X).reshape(1,-1)
	# print ('\n测评(loss)：')
	# print (model.evaluate(Test_X, Test_Y))
	# print ('\n预测(test)：')
	# print (Result)
	# print ('\n真实(test)：')
	# print (Test_Y)
	# print ('\n预测：')
	# print (Prediction)
	# print (Result)
	key = StockName + " Next Day Value"

	json_data = {
			key: Result[0][0].tolist()
	}

	print(json_data)
	json_path = './ANN prediction.json'
	with open(json_path, "w") as f:
		json.dump(json_data, f)
		print("Complete...")


def main():
	companyNameList = ["GOOG","AABA","AMZN","OPK","FB","TWTR","NFLX","TSLA","BABA","SPLK"]
	# print(companyNameList)
	# print("Please input the company name: ")
	# name = input()
	# ANNPredict(name)
	for com in companyNameList:
		ANNPredict(com)
		

if __name__ == '__main__':
	main()
# written by: ZE LIU
# assisted by: Xinyu Lyu
# debugged by: All members

from sklearn import svm
import csv
from sqlalchemy import create_engine
import pandas as pd
import json


def SVMPredict(StockName):
	engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/TESTDB')
	df = pd.read_sql_query('SELECT * FROM '+StockName+'_History_Price', engine)
	newData = df.values.T.tolist()

	# newData is a big list of the history price and we only need close price now
	ClosePrice = newData[4]
	for i in range(0, len(ClosePrice)):
		ClosePrice[i] = float(ClosePrice[i])
	

	BigTimeData = []
	i = 1
	for r in range(0,len(ClosePrice)):
		SmallTimeData = [i]
		BigTimeData.append(SmallTimeData)
		i = i + 1

	# print(ClosePrice);
	# print();
	# print(BigTimeData);
	# except Exception as e:
	# 	# raise e
	# 	print("Error: No such file")
	# else:
	# 	print("Succeed in reading such file")
	

	# X = [[0], [2]]
	# y = [0.5, 2.5]
	# NextDay = [[1]]
	clf = svm.SVR()
	NextDay = [[len(ClosePrice)]]
	# clf.fit(X, y) 
	clf.fit(BigTimeData, ClosePrice) 
	# SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
	#     kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
	Result = clf.predict(NextDay)
	# print(Result)

	key = StockName + " Next Day Value"
	json_data = {
	        key: float(Result)
	}

	# Json result: {'Next Day Value': Price}
	print(json_data)

	json_path = './SVM prediction.json'
	with open(json_path, "w") as f:
		json.dump(json_data, f)
		print("Complete...")



def main():
    companyNameList = ["GOOG","AABA","AMZN","OPK","FB","TWTR","NFLX","TSLA","BABA","SPLK"]
    # print(companyNameList)
    # print("Please input the company name: ")
    # name = input()
    # SVMPredict(name)
    for com in companyNameList:
    	SVMPredict(com)

if __name__ == '__main__':
	main()
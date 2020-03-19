# ECE568
## Rutgers SOFTWR ENGG WEB APPL ECE 568
Developed By:
Ze liu Tong Wu Xinyu Lyu Xinwei Zhao Jay Borkar

For the “design” file, it is our UML diagrams. For the “code” file, it contains our back-end files. Such as the Python inside the “code” file, it contains flask, ANN predictor, LSTM predictor, SVM predictor and the Indicator function. Flask is used to do the registration and login in. When user want to apply for a new account, we will save his Email and corresponding password into the MySQL table: “user”. And also create a table using the email of user to save the company he/she like. The Java file contains Bayesian Curve Fitting predictor and the Web Service. It also contains the whole project of the web service. Below is the description of our web service.
Programming language: Java

IDE: Eclipse

Framework: Restful with JAX-RS

The folder contains both the source code of the web service interface and the whole web project of the web interface.
"StockResource.java" contains all the Get functions along with the URL of Restful JAX-RS. The functions respond to different client requests by calling the specific URL/path. Then it gives the response to the client with the specific message the client requested before in JSON format files. We implement the query functions to fully satisfy the Query functions on the final project requirement, such as show the list of all companies in the database along with their latest price. Besides, in order to draw the stock history/real price diagrams, we implement the functions to return the JSON files containing the history/real-time stock information to the clients. "StockService.java" contains the basic search functions to connect to the MySQL Database and fetch the result from the database to the Get functions in "StockResource.java". Actually, we implement the MySQL statements we need, then build the JSON format and return the messages in such format to the web front from the back. And the basic functions include all the query functions in final project requirement. Also, in order to draw the stock history/real price diagrams, we implement the functions to return the JSON files containing the history/real-time stock information to the clients.

"pom.xml" contains all the maven dependencies like MySQL-connector-java, org.json to support the project.
“images” are just some icons for the websites. “data” file contains the all the real-time price and history price of the ten company. Besides, it contains the 30 indicators data (each company have three corresponding indicators: ROC, BOV, MACD). These are all csv format. The “run” file contains our HTML. The corresponding resources are also contained. “echart” file is the function to draw a chart in website.

Run our project, make sure you already install all the packages, otherwise use pip3 to install it. Change the chrome driver path in our code with yours. Install the MySQL server and Workbench so that we can connect to your own database. Then, create a database in Mysql called: TESTDB. All the tables will be saved into this database. After that, open terminal, cd to the file “application” and enter “python3 Flask_Back.py” to simply run the service.
Type the address " http://127.0.0.1:8088/preRegist" to enter the website. Then you can register your own account the login in. For our special feature, we create a table using the user’s account when he / she created the account. And this table contains the his / her favorite stocks.

The file Stock Data contains 10 companies’ stock information. The history file contains up to 20 years of the historical prices. The real time data contains the latest day’s price and the time slice between two real-time points is about 1 minutes.

![avatar](https://github.com/XinyuLyu/ECE568/blob/master/1.png)
![avatar](https://github.com/XinyuLyu/ECE568/blob/master/2.png)
![avatar](https://github.com/XinyuLyu/ECE568/blob/master/3.png)
![avatar](https://github.com/XinyuLyu/ECE568/blob/master/4.png)
![avatar](https://github.com/XinyuLyu/ECE568/blob/master/5.png)
![avatar](https://github.com/XinyuLyu/ECE568/blob/master/6.png)
![avatar](https://github.com/XinyuLyu/ECE568/blob/master/7.png)

# written by: ZE LIU, Tong Wu
# assisted by: All members
# debugged by: All members

import Get_History
import Get_Realtime
companyNameList = ["GOOG","AABA","AMZN","OPK","FB",
                   "TWTR","NFLX","TSLA","BABA","SPLK"]
                   
def main():
    print("Welcome! Please select the option:")
    print("1. Get History Price")
    print("2. Get Realtime Price" )
    choice = input()
    if choice == "1":
        print("Please input the company name: ")
        print(companyNameList)
        name = input()
        url = "https://finance.yahoo.com/quote/"+name+"/history?p="+name
        Get_History.main(url,name)
    if choice == "2":
        print("Please input the company name: ")
        print(companyNameList)
        name = input()
        url = "https://finance.yahoo.com/quote/"+name+"?p="+name
        Get_Realtime.main(url,name)


if __name__ == '__main__':
    main()



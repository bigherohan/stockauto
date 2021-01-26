import os, sys, ctypes
import win32com.client
import pandas as pd
from datetime import datetime
from slacker import Slacker
import time, calendar



import win32com.client

 



getcode = ['A005950',"A267320","A124560","A005935","A102460","A055550","A024880","A179290","A067010","A005950"]
buycode = []
sellcode = []
# for code in codeList:
#     getcode.append(code)

#for code in codeList2:
#    getcode.append(code)
#getcode.append(codeList)
#getcode. append(codeList2)

#print(getcode)


#2. 종목선정 필터링 거치기

#getcode 에서 하나씩 꺼내와서 i 에 넣은 후 예상종가,내일예상종가를 받아야된다
class filtering() :
    for i in getcode:
        #print(i)
        # 현재가 객체 구하기
        objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
        objStockMst.SetInputValue(0, i)   #종목 코드 - 
        objStockMst.BlockRequest()
        
        #현재가 통신 및 통신 에러 처리 
        rqStatus = objStockMst.GetDibStatus()
        rqRet = objStockMst.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()
        # 현재가 정보 조회
        code = objStockMst.GetHeaderValue(0)  #종목코드
        name= objStockMst.GetHeaderValue(1)  # 종목명
        time= objStockMst.GetHeaderValue(4)  #시 간
        price= objStockMst.GetHeaderValue(11) # 현재가
        diff= objStockMst.GetHeaderValue(12)  # 전일종가대비현재가
        open= objStockMst.GetHeaderValue(13)  # 시가
        high= objStockMst.GetHeaderValue(14)  # 고가
        low= objStockMst.GetHeaderValue(15)   # 저가
        offer = objStockMst.GetHeaderValue(16)  #매도호가
        bid = objStockMst.GetHeaderValue(17)   #매수호가
        vol= objStockMst.GetHeaderValue(18)   #거래량
        vol_value= objStockMst.GetHeaderValue(19)  #거래대금
        high52 = objStockMst.GetHeaderValue(47)    #52주고가
        yestcp =  objStockMst.GetHeaderValue(10) #전일종가
        low52 = objStockMst.GetHeaderValue(49)  #52주저가

        #print("현재가 : " , price)


        #print(yestcp*((open-yestcp) / yestcp)) #수식1  (양수화 안돼서 결과값이 마이너스임)
        predict11 = (yestcp*((open-yestcp) / yestcp))   #predict1 에 수식1 넣음
        #print(predict11)    
        
        stand1 = min(open,price,yestcp) #기준가

        #print(stand1*((stand1/high52)) #수식2
        predict12 = (stand1 * (stand1 / high52))  #predict2 에 수식 2 넣음
        #print((high52-stand1)*(stand1/high52)) #수식3
        predict13 = (high52-stand1)*(stand1/high52) #predict3 에 수식 3넣음

        #print(predict13)

        #print('예상종가',predict11 + predict12 + predict13)
        predictday = predict11 + predict12 + predict13
        print('예상종가',predictday)

        ##내일예상종가
        stand2 = predictday #기준가 = 예상종가
        #print(yestcp*((open-yestcp) / yestcp)) #수식1  
        predict21 = (stand2*((open-yestcp) / yestcp))   #predict1 에 수식1 넣음

        #print(stand1*((stand1/high52)) #수식2
        predict22 = (stand1 * (stand1 / high52))  #predict2 에 수식 2 넣음

        #print((high52-stand1)*(stand1/high52)) #수식3
        predict23 = (high52-stand1)*(stand1/high52) #predict3 에 수식 3넣음

        #print(predict3)

        #print('내일예상종가',predict21 + predict22 + predict23)

        predictto = (predict21 + predict22 + predict23)
        print('내일예상종가',predictto)

        print("------------------")
        if price < predictday and predictday < predictto:
            buycode.append(code) #매수종목
        elif price < predictday and predictday >= predictto:
            sellcode.append(code) #매도종목
        #print(i, name)
    print("매수종목코드" + str(buycode))
    print("매도종목코드" + str(sellcode))


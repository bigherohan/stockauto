import win32com.client
 
# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 
# 현재가 객체 구하기
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
objStockMst.SetInputValue(0, 'A005930')   #종목 코드 - 삼성전자
objStockMst.BlockRequest()

 
# 현재가 통신 및 통신 에러 처리 
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


# 예상 체결관련 정보
exFlag = objStockMst.GetHeaderValue(58) #예상체결가 구분 플래그
exPrice = objStockMst.GetHeaderValue(55) #예상체결가
exDiff = objStockMst.GetHeaderValue(56) #예상체결가 전일대비
exVol = objStockMst.GetHeaderValue(57) #예상체결수량
 
 
print("코드", code)
print("이름", name)
print("시간", time)
print("현재가", price)
print("전일종가대비현재가", diff)
print("시가", open)
print("고가", high)
print("저가", low)
print("매도호가", offer)
print("매수호가", bid)
print("거래량", vol)
print("거래대금", vol_value)
print('52주고가', high52)
print('52주저가',low52)
print('전일종가', yestcp) 

if (exFlag == ord('0')):
    print("장 구분값: 동시호가와 장중 이외의 시간")
elif (exFlag == ord('1')) :
    print("장 구분값: 동시호가 시간")
elif (exFlag == ord('2')):
    print("장 구분값: 장중 또는 장종료")
 
print("예상체결가 대비 수량")
print("예상체결가", exPrice)
print("예상체결가 대비", exDiff)
print("예상체결수량", exVol)

#전일대비= (전일종가-개장가)/전일종가
#diffo = (yestcp-open)/yestcp

#예상종가 = 수식1 + 수식2 + 수식3
#stand1(기준가) = min(open,price,yestcp)

#수식1 = "((전일종가*전일대비%((*양수화)))"
#수식2 = "(기준가*(기준가/52주최고가%)"
#수식3 = "((기준가/52주최고가%)*(52최고가-기준가(*양수화))))"


#수식1 = "((yestcp*((open-yestcp)/yestcp)((*양수화)))"
#수식2 = "( min(open,price,yestcp)*( min(open,price,yestcp)/high52)"
#수식3 = "(( min(open,price,yestcp)/high52%)*(high52- min(open,price,yestcp)(*양수화))))"



#print(yestcp*((open-yestcp) / yestcp)) #수식1  (양수화 안돼서 결과값이 마이너스임)
predict11 = (yestcp*((open-yestcp) / yestcp))   #predict1 에 수식1 넣음

stand1 = min(open,price,yestcp) #기준가



#print(stand1*((stand1/high52)) #수식2
predict12 = (stand1 * (stand1 / high52))  #predict2 에 수식 2 넣음



#print((high52-stand1)*(stand1/high52)) #수식3
predict13 = (high52-stand1)*(stand1/high52) #predict3 에 수식 3넣음

#print(predict3)

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

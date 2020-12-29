objStockMst.GetHeaderValue() 

code = objStockMst.GetHeaderValue(0)  #종목코드
name= objStockMst.GetHeaderValue(1)  # 종목명
time= objStockMst.GetHeaderValue(4)  # 시간
price= objStockMst.GetHeaderValue(11) # 현재가
diff= objStockMst.GetHeaderValue(12)  # 대비
open= objStockMst.GetHeaderValue(13)  # 시가
high= objStockMst.GetHeaderValue(14)  # 고가
low= objStockMst.GetHeaderValue(15)   # 저가
offer = objStockMst.GetHeaderValue(16)  #매도호가
bid = objStockMst.GetHeaderValue(17)   #매수호가
vol= objStockMst.GetHeaderValue(18)   #거래량
vol_value= objStockMst.GetHeaderValue(19)  #거래대금
high52 = objStockMst.GetHeaderValue(47)    #52주고가
low52 = objStockMst.GetHeaderValue(49)  #52주저가
yestcp =  objStockMst.GetHeaderValue(10) #전일종가


#전일대비= (전일종가-개장가)/전일종가
#diffo = (yestcp-open)/yestcp

#예상종가 = 수식1 + 수식2 + 수식3
#stand1(기준가) = min(open,price,yestcp)

#수식1 = "((전일종가*전일대비%((*양수화)))"
#수식2 = "(기준가*(기준가/52주최고가%)"
#수식3 = "((기준가/52주최고가%)*(52최고가-기준가(*양수화))))"


#수식1 = "((yestcp*((yestcp-open)/yestcp)((*양수화)))"
#수식2 = "( min(open,price,yestcp)*( min(open,price,yestcp)/high52%)"
#수식3 = "(( min(open,price,yestcp)/high52%)*(high52- min(open,price,yestcp)(*양수화))))"

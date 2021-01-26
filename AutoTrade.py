import os, sys, ctypes
import win32com.client
import pandas as pd
from datetime import datetime
from slacker import Slacker
import time, calendar



import win32com.client

 
 
# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 
# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1) #거래소
codeList2 = objCpCodeMgr.GetStockListByMarket(2) #코스닥

print(type(codeList)) 

print("거래소 종목코드", len(codeList))
for i, code in enumerate(codeList):
    secondCode = objCpCodeMgr.GetStockSectionKind(code)
    name = objCpCodeMgr.CodeToName(code)
    stdPrice = objCpCodeMgr.GetStockStdPrice(code)
    #print(i, code, secondCode, stdPrice, name)
 
#print("코스닥 종목코드", len(codeList2))
for i, code in enumerate(codeList2):
    secondCode = objCpCodeMgr.GetStockSectionKind(code)
    name = objCpCodeMgr.CodeToName(code)
    stdPrice = objCpCodeMgr.GetStockStdPrice(code)
    #print(i, code, secondCode, stdPrice, name)
 
#print("거래소 + 코스닥 종목코드 ",len(codeList) + len(codeList2))




getcode = ["A024810","A000890","A004060","A004410","A004920","A005030","A008040"]
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

for i in getcode:
    print(i)
    # 현재가 객체 구하기
    objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
    objStockMst.SetInputValue(0, i)   #종목 코드 - 삼성전자
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

    print("현재가 : " , price)


    #print(yestcp*((open-yestcp) / yestcp)) #수식1  (양수화 안돼서 결과값이 마이너스임)
    predict11 = (yestcp*((open-yestcp) / yestcp))   #predict1 에 수식1 넣음
    #print(predict11)    
    
    stand1 = min(open,price,yestcp) #기준가

    #print(stand1*((stand1/high52)) #수식2
    predict12 = (stand1 * (stand1 / high52))  #predict2 에 수식 2 넣음
    #print((high52-stand1)*(stand1/high52)) #수식3
    predict13 = (high52-stand1)*(stand1/high52) #predict3 에 수식 3넣음

    #print(predict13)

    print('예상종가',predict11 + predict12 + predict13)
    predictday = predict11 + predict12 + predict13
    #print('예상종가',predictday)

    ##내일예상종가
    stand2 = predictday #기준가 = 예상종가
    #print(yestcp*((open-yestcp) / yestcp)) #수식1  
    predict21 = (stand2*((open-yestcp) / yestcp))   #predict1 에 수식1 넣음

    #print(stand1*((stand1/high52)) #수식2
    predict22 = (stand1 * (stand1 / high52))  #predict2 에 수식 2 넣음

    #print((high52-stand1)*(stand1/high52)) #수식3
    predict23 = (high52-stand1)*(stand1/high52) #predict3 에 수식 3넣음

    #print(predict3)

    print('내일예상종가',predict21 + predict22 + predict23)

    predictto = (predict21 + predict22 + predict23)
    #print('내일예상종가',predictto)

    print("------------------")
    if price < predictday and predictday < predictto:
        buycode.append(code) #매수종목
    elif price < predictday and predictday >= predictto:
        sellcode.append(code) #매도종목
    #print(i, code)

print("매수종목코드" + str(buycode))
print("매도종목코드" + str(sellcode))


targetcode = buycode



import os, sys, ctypes
import win32com.client
import pandas as pd
from datetime import datetime
from slacker import Slacker
import time, calendar

slack = Slacker('xoxb-1584909758453-1626951052036-8HN6qf9oF3NkAPTGLxn1gxZD')
def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    slack.chat.post_message('stock', strbuf)

def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)
 
# 크레온 플러스 공통 OBJECT
cpCodeMgr = win32com.client.Dispatch('CpUtil.CpStockCode')
cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
cpStock = win32com.client.Dispatch('DsCbo1.StockMst')
cpOhlc = win32com.client.Dispatch('CpSysDib.StockChart')
cpBalance = win32com.client.Dispatch('CpTrade.CpTd6033')
cpCash = win32com.client.Dispatch('CpTrade.CpTdNew5331A')
cpOrder = win32com.client.Dispatch('CpTrade.CpTd0311')  

def check_creon_system():
    """크레온 플러스 시스템 연결 상태를 점검한다."""
    # 관리자 권한으로 프로세스 실행 여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        printlog('check_creon_system() : admin user -> FAILED')
        return False
 
    # 연결 여부 체크
    if (cpStatus.IsConnect == 0):
        printlog('check_creon_system() : connect to server -> FAILED')
        return False
 
    # 주문 관련 초기화 - 계좌 관련 코드가 있을 때만 사용
    if (cpTradeUtil.TradeInit(0) != 0):
        printlog('check_creon_system() : init trade -> FAILED')
        return False
    return True

def get_current_price(code):
    """인자로 받은 종목의 현재가, 매수호가, 매도호가를 반환한다."""
    cpStock.SetInputValue(0, code)  # 종목코드에 대한 가격 정보
    cpStock.BlockRequest()
    item = {}
    item['cur_price'] = cpStock.GetHeaderValue(11)   # 현재가
    item['ask'] =  cpStock.GetHeaderValue(16)        # 매수호가
    item['bid'] =  cpStock.GetHeaderValue(17)        # 매도호가    
    return item['cur_price'], item['ask'], item['bid']

def get_ohlc(code, qty):
    """인자로 받은 종목의 OHLC 가격 정보를 qty 개수만큼 반환한다."""
    cpOhlc.SetInputValue(0, code)           # 종목코드
    cpOhlc.SetInputValue(1, ord('2'))        # 1:기간, 2:개수
    cpOhlc.SetInputValue(4, qty)             # 요청개수
    cpOhlc.SetInputValue(5, [0, 2, 3, 4, 5]) # 0:날짜, 2~5:OHLC
    cpOhlc.SetInputValue(6, ord('D'))        # D:일단위
    cpOhlc.SetInputValue(9, ord('1'))        # 0:무수정주가, 1:수정주가
    cpOhlc.BlockRequest()
    count = cpOhlc.GetHeaderValue(3)   # 3:수신개수
    columns = ['open', 'high', 'low', 'close']
    index = []
    rows = []
    for i in range(count): 
        index.append(cpOhlc.GetDataValue(0, i)) 
        rows.append([cpOhlc.GetDataValue(1, i), cpOhlc.GetDataValue(2, i),
            cpOhlc.GetDataValue(3, i), cpOhlc.GetDataValue(4, i)]) 
    df = pd.DataFrame(rows, columns=columns, index=index) 
    return df

def get_stock_balance(code):
    """인자로 받은 종목의 종목명과 수량을 반환한다."""
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0]      # 계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1) # -1:전체, 1:주식, 2:선물/옵션
    cpBalance.SetInputValue(0, acc)         # 계좌번호
    cpBalance.SetInputValue(1, accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
    cpBalance.SetInputValue(2, 50)          # 요청 건수(최대 50)
    cpBalance.BlockRequest()     
    if code == 'ALL':
        dbgout('계좌명: ' + str(cpBalance.GetHeaderValue(0)))
        dbgout('결제잔고수량 : ' + str(cpBalance.GetHeaderValue(1)))
        dbgout('평가금액: ' + str(cpBalance.GetHeaderValue(3)))
        dbgout('평가손익: ' + str(cpBalance.GetHeaderValue(4)))
        dbgout('종목수: ' + str(cpBalance.GetHeaderValue(7)))
    stocks = []
    for i in range(cpBalance.GetHeaderValue(7)):
        stock_code = cpBalance.GetDataValue(12, i)  # 종목코드
        stock_name = cpBalance.GetDataValue(0, i)   # 종목명
        stock_qty = cpBalance.GetDataValue(15, i)   # 수량
        if code == 'ALL':
            dbgout(str(i+1) + ' ' + stock_code + '(' + stock_name + ')' 
                + ':' + str(stock_qty))
            stocks.append({'code': stock_code, 'name': stock_name, 
                'qty': stock_qty})
        if stock_code == code:  
            return stock_name, stock_qty
    if code == 'ALL':
        return stocks
    else:
        stock_name = cpCodeMgr.CodeToName(code)
        return stock_name, 0

def get_current_cash():
    """증거금 100% 주문 가능 금액을 반환한다."""
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0]    # 계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1) # -1:전체, 1:주식, 2:선물/옵션
    cpCash.SetInputValue(0, acc)              # 계좌번호
    cpCash.SetInputValue(1, accFlag[0])      # 상품구분 - 주식 상품 중 첫번째
    cpCash.BlockRequest() 
    return cpCash.GetHeaderValue(9) # 증거금 100% 주문 가능 금액

def get_target_price(code):
    """매수 목표가를 반환한다."""
    try:
        time_now = datetime.now()
        str_today = time_now.strftime('%Y%m%d')
        ohlc = get_ohlc(code, 10)
        if str_today == str(ohlc.iloc[0].name):
            today_open = ohlc.iloc[0].open 
            lastday = ohlc.iloc[1]
        else:
            lastday = ohlc.iloc[0]                                      
            today_open = lastday[3]
        lastday_high = lastday[1]
        lastday_low = lastday[2]
        target_price = today_open + (lastday_high - lastday_low) * 0.5
        return target_price
    except Exception as ex:
        dbgout("`get_target_price() -> exception! " + str(ex) + "`")
        return None
    
def get_movingaverage(code, window):
    """인자로 받은 종목에 대한 이동평균가격을 반환한다."""
    try:
        time_now = datetime.now()
        str_today = time_now.strftime('%Y%m%d')
        ohlc = get_ohlc(code, 20)
        if str_today == str(ohlc.iloc[0].name):
            lastday = ohlc.iloc[1].name
        else:
            lastday = ohlc.iloc[0].name
        closes = ohlc['close'].sort_index()         
        ma = closes.rolling(window=window).mean()
        return ma.loc[lastday]
    except Exception as ex:
        dbgout('get_movingavrg(' + str(window) + ') -> exception! ' + str(ex))
        return None    

def buy_etf(code):
    """인자로 받은 종목을 최유리 지정가 FOK 조건으로 매수한다."""
    try:
        global bought_list      # 함수 내에서 값 변경을 하기 위해 global로 지정
        if code in bought_list: # 매수 완료 종목이면 더 이상 안 사도록 함수 종료
            #printlog('code:', code, 'in', bought_list)
            return False
        time_now = datetime.now()
        current_price, ask_price, bid_price = get_current_price(code) 
        target_price = get_target_price(code)    # 매수 목표가
        ma5_price = get_movingaverage(code, 5)   # 5일 이동평균가
        ma10_price = get_movingaverage(code, 10) # 10일 이동평균가
        buy_qty = 0        # 매수할 수량 초기화
        if ask_price > 0:  # 매수호가가 존재하면   
            buy_qty = buy_amount // ask_price  
        stock_name, stock_qty = get_stock_balance(code)  # 종목명과 보유수량 조회
        #printlog('bought_list:', bought_list, 'len(bought_list):',
        #    len(bought_list), 'target_buy_count:', target_buy_count)     
        if current_price > target_price and current_price > ma5_price \
            and current_price > ma10_price:  
            printlog(stock_name + '(' + str(code) + ') ' + str(buy_qty) +
                'EA : ' + str(current_price) + ' meets the buy condition!`')            
            cpTradeUtil.TradeInit()
            acc = cpTradeUtil.AccountNumber[0]      # 계좌번호
            accFlag = cpTradeUtil.GoodsList(acc, 1) # -1:전체,1:주식,2:선물/옵션                
            # 최유리 FOK 매수 주문 설정
            cpOrder.SetInputValue(0, "2")        # 2: 매수
            cpOrder.SetInputValue(1, acc)        # 계좌번호
            cpOrder.SetInputValue(2, accFlag[0]) # 상품구분 - 주식 상품 중 첫번째
            cpOrder.SetInputValue(3, code)       # 종목코드
            cpOrder.SetInputValue(4, buy_qty)    # 매수할 수량
            cpOrder.SetInputValue(7, "2")        # 주문조건 0:기본, 1:IOC, 2:FOK
            cpOrder.SetInputValue(8, "12")       # 주문호가 1:보통, 3:시장가
                                                 # 5:조건부, 12:최유리, 13:최우선 
            # 매수 주문 요청
            ret = cpOrder.BlockRequest() 
            printlog('최유리 FoK 매수 ->', stock_name, code, buy_qty, '->', ret)
            if ret == 4:
                remain_time = cpStatus.LimitRequestRemainTime
                printlog('주의: 연속 주문 제한에 걸림. 대기 시간:', remain_time/1000)
                time.sleep(remain_time/1000) 
                return False
            time.sleep(2)
            printlog('현금주문 가능금액 :', buy_amount)
            stock_name, bought_qty = get_stock_balance(code)
            printlog('get_stock_balance :', stock_name, stock_qty)
            if bought_qty > 0:
                bought_list.append(code)
                dbgout("`buy_etf("+ str(stock_name) + ' : ' + str(code) + 
                    ") -> " + str(bought_qty) + "EA bought!" + "`")
    except Exception as ex:
        dbgout("`buy_etf("+ str(code) + ") -> exception! " + str(ex) + "`")

def sell_all():
    """보유한 모든 종목을 최유리 지정가 IOC 조건으로 매도한다."""
    try:
        cpTradeUtil.TradeInit()
        acc = cpTradeUtil.AccountNumber[0]       # 계좌번호
        accFlag = cpTradeUtil.GoodsList(acc, 1)  # -1:전체, 1:주식, 2:선물/옵션   
        while True:    
            stocks = get_stock_balance('ALL') 
            total_qty = 0 
            for s in stocks:
                total_qty += s['qty'] 
            if total_qty == 0:
                return True
            for s in stocks:
                if s['qty'] != 0:                  
                    cpOrder.SetInputValue(0, "1")         # 1:매도, 2:매수
                    cpOrder.SetInputValue(1, acc)         # 계좌번호
                    cpOrder.SetInputValue(2, accFlag[0])  # 주식상품 중 첫번째
                    cpOrder.SetInputValue(3, s['code'])   # 종목코드
                    cpOrder.SetInputValue(4, s['qty'])    # 매도수량
                    cpOrder.SetInputValue(7, "1")   # 조건 0:기본, 1:IOC, 2:FOK
                    cpOrder.SetInputValue(8, "12")  # 호가 12:최유리, 13:최우선 
                    # 최유리 IOC 매도 주문 요청
                    ret = cpOrder.BlockRequest()
                    printlog('최유리 IOC 매도', s['code'], s['name'], s['qty'], 
                        '-> cpOrder.BlockRequest() -> returned', ret)
                    if ret == 4:
                        remain_time = cpStatus.LimitRequestRemainTime
                        printlog('주의: 연속 주문 제한, 대기시간:', remain_time/1000)
                time.sleep(1)
            time.sleep(30)
    except Exception as ex:
        dbgout("sell_all() -> exception! " + str(ex))

if __name__ == '__main__': 
    try:
        symbol_list = [buycode]
        bought_list = []     # 매수 완료된 종목 리스트
        target_buy_count = 5 # 매수할 종목 수
        buy_percent = 0.19   
        printlog('check_creon_system() :', check_creon_system())  # 크레온 접속 점검
        stocks = get_stock_balance('ALL')      # 보유한 모든 종목 조회
        total_cash = int(get_current_cash())   # 100% 증거금 주문 가능 금액 조회
        buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
        printlog('100% 증거금 주문 가능 금액 :', total_cash)
        printlog('종목별 주문 비율 :', buy_percent)
        printlog('종목별 주문 금액 :', buy_amount)
        printlog('시작 시간 :', datetime.now().strftime('%m/%d %H:%M:%S'))
        soldout = False

        while True:
            t_now = datetime.now()
            t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
            t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
            t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
            t_exit = t_now.replace(hour=15, minute=20, second=0,microsecond=0)
            today = datetime.today().weekday()
            if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
                printlog('Today is', 'Saturday.' if today == 5 else 'Sunday.')
                sys.exit(0)
            if t_9 < t_now < t_start and soldout == False:
                soldout = True
                sell_all()
            if t_start < t_now < t_sell :  # AM 09:05 ~ PM 03:15 : 매수
                for sym in symbol_list:
                    if len(bought_list) < target_buy_count:
                        buy_etf(sym)
                        time.sleep(1)
                if t_now.minute == 30 and 0 <= t_now.second <= 5: 
                    get_stock_balance('ALL')
                    time.sleep(5)
            if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 일괄 매도
                if sell_all() == True:
                    dbgout('`sell_all() returned True -> self-destructed!`')
                    sys.exit(0)
            if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
                dbgout('`self-destructed!`')
                sys.exit(0)
            time.sleep(3)
    except Exception as ex:
        dbgout('`main -> exception! ' + str(ex) + '`')
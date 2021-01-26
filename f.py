
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
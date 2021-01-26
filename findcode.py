import win32com.client
 
# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 

#whatname = ("삼성전자") #종목명
objCpStockCode = win32com.client.Dispatch("cpUtil.CpStockCode")
#objCpStockCode.SetInputValue(0,)   #종목 코드 


codename = "한국유니온제약"   #찾을 종목명 입력!!
namecode = objCpStockCode.NameToCode(str(codename))
print(str(codename) + str(namecode))

#objCpStockCode.BlockRequest()
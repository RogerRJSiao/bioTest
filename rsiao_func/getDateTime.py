# 設定時間戳記
from datetime import datetime,timezone,timedelta

#取得當時日期時刻
def getDateTime_now():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    return dt1, dt2

def showDateTime_utc():
    dt1, dt2 = getDateTime_now()
    print('UTC \t%s\nUTC+8\t%s'%(dt1,dt2))
    print(dt2.strftime("%Y-%m-%d %H:%M:%S")) # 將時間轉換為 string

def showDateTime():
    dt1, dt2 = getDateTime_now()
    print(dt2.strftime("%Y-%m-%d %H:%M:%S")) # 將時間轉換為 string

def renameDate(fileName):
    timestamp = dt2.strftime("%Y%m%d")
    fileName += timestamp
    print("檔名更新，已加上:", timestamp)
    return fileName

def renameTime(fileName):
    timestamp = dt2.strftime("%H%M%S")
    fileName += timestamp
    print("檔名更新，已加上:", timestamp)
    return fileName

def renameDateTime(fileName):
    timestamp = dt2.strftime("%Y%m%d_%H%M%S")
    fileName += timestamp
    print("檔名更新，已加上:", timestamp)
    return fileName
# 設定時間戳記
from datetime import datetime,timezone,timedelta

#取得當時日期時刻
def getDateTime_now():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    return dt1, dt2

#顯示UTC時刻
def showDateTime_utc():
    dt1, dt2 = getDateTime_now()
    print('UTC \t%s\nUTC+8\t%s'%(dt1,dt2))
    print(dt2.strftime("%Y-%m-%d %H:%M:%S")) # 將時間轉換為 string
    print('AAA')

#顯示UTC+8時刻
def showDateTime():
    dt1, dt2 = getDateTime_now()
    print(dt2.strftime("%Y-%m-%d %H:%M:%S")) # 將時間轉換為 string

#重新命名+時間戳記
def rename_timestamp(fileName, dt_format):
    dt1, dt2 = getDateTime_now()
    fileName = fileName.split('.', 1 )
    match dt_format:
        case 'date': 
            timestamp = dt2.strftime("_%Y%m%d")
        case 'time':
            timestamp = dt2.strftime("_%H%M%S")
        case _:
            timestamp = dt2.strftime("_%Y%m%d_%H%M%S")
    fileName = fileName[0] + timestamp + "." + fileName[1]
    print("檔名更新，已加上:", timestamp)
    return fileName
from datetime import datetime, time, timedelta
from dateutil.relativedelta import relativedelta

# 指定日時前のAM6時(基準時間)を取得
def get_standard_dt(days=0, months=0):
    # monthsヶ月、days日前の現在時刻を取得
    dt = datetime.now() - relativedelta(months=months) - timedelta(days=days)

    # 直前のAM6時(基準時間)を取得
    if dt.time() < time(hour=6):
        dt -= timedelta(days=1)

    standard_dt = dt.replace(hour=6,minute=0,second=0,microsecond=0)
    print(f'standard_dt : {standard_dt}')

    return standard_dt


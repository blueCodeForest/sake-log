from datetime import datetime, time, timedelta
from dateutil.relativedelta import relativedelta

# 指定日時前のAM6時(基準時間)を取得
def get_standard_dt(days=0, months=0):
    # monthsヶ月、days日前の現在時刻を取得
    standard_dt = datetime.now() - relativedelta(months=months) - timedelta(days=days)

    # 直前のAM6時(基準時間)を取得
    if standard_dt.time() < time(hour=6):
        standard_dt -= timedelta(days=1)

    standard_dt.replace(hour=6,minute=0,second=0,microsecond=0)

    return standard_dt


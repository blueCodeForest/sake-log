# date.py -> 日付に関する処理

import datetime
from dateutil.relativedelta import relativedelta
from dateutil import tz

from .models import AlcoholLogList


# 指定日時前のAM6時(基準時間)を取得
# datetime(UTC), int -> datetime(JST)
def get_am6_dt(dt=datetime.datetime.now(), days=0, months=0):
    
    # タイムゾーンを'Asia/Tokyo'に設定
    dt = dt.astimezone(tz.gettz('Asia/Tokyo'))

    # dtからmonthsヶ月、days日さかのぼる
    dt -= (relativedelta(months=months) + datetime.timedelta(days=days))

    # 基準時間分巻き戻す。
    # 例)1月3日0時5分のデータを3日ではなく2日扱いにするため。
    # 0時をまたいで飲んだ時にリセットされたら意味がない。
    dt -= datetime.timedelta(hours=6)

    # 日付はそのままでAM6時にする
    am6_dt = dt.replace(hour=6,minute=0,second=0,microsecond=0)

    return am6_dt

# 指定期間前のdatetimeオブジェクトを返す
# str -> datetime
def get_start_day(term):
    dt = datetime.datetime.now()

    if term == 'all':
        start_dt = get_am6_dt(AlcoholLogList.objects.earliest('created_at').created_at)
    elif term == 'half_year':
        start_dt = get_am6_dt(months=6)
    elif term == 'month':
        start_dt = get_am6_dt(months=1)
    elif term == 'week':
        start_dt = get_am6_dt(days=6)
    elif term == 'today':
        start_dt = get_am6_dt()

    return start_dt

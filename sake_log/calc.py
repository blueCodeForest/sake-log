# calc.py -> データを加工する処理

import datetime
from dateutil.relativedelta import relativedelta
from dateutil import tz

from .models import AlcoholLogList
from .date import get_am6_dt

# 正味アルコール摂取量を合計する
def get_sum_alcohol_amount(request):
        drinks = AlcoholLogList.objects.filter(user=request.user, created_at__gte=get_am6_dt())
        sum_alcohol_amount = 0
        for drink in drinks:
            sum_alcohol_amount += drink.get_1cup_alcohol_amount()
        sum_alcohol_amount = round(sum_alcohol_amount)
        return sum_alcohol_amount

# クエリセットを期間に応じて辞書に加工する
def qs_to_dict(qs, term):
    qs_dict = {}
    sum_alcohol = 0

    # 日付ごとにアルコール量を集計する
    if term in ['week', 'month', 'half_year']:
        # クエリセットからクエリをひとつずつ取り出す
        for i in range(qs.count()):
            # アルコール量を加算
            sum_alcohol += qs[i].get_1cup_alcohol_amount()

            # 次のクエリが存在するか確認
            if i + 1 < len(qs):
                
                # 次のクエリと日付が異なればデータに反映し、アルコール量をリセット
                if get_am6_dt(qs[i].created_at) != get_am6_dt(qs[i+1].created_at):
                    qs_dict[get_am6_dt(qs[i].created_at).date()] = sum_alcohol
                    sum_alcohol = 0

            # 最後のクエリのデータを反映させる
            else:
                qs_dict[get_am6_dt(qs[i].created_at).date()] = sum_alcohol
    
    return qs_dict

# 飲まなかった日に0のデータを追加する
def zero_fill_date(qs_dict, days=0, months=0):
    dt_now = get_am6_dt(datetime.datetime.now()).date()
    dt = dt_now - relativedelta(months=months) - datetime.timedelta(days=days)
    date_dict = {}

    while dt <= dt_now:
        date_dict[dt] = 0
        dt += datetime.timedelta(days=1)

    for key in date_dict:
        if key in qs_dict:
            date_dict[key] = qs_dict[key]

    return date_dict

# 飲まなかった日、月に0のデータを追加する
# zero_fillの前準備
def zero_fill(qs_dict, term):
    if term == 'week':
        graph_data_dict = zero_fill_date(qs_dict, days=6)
    elif term == 'month':
        graph_data_dict = zero_fill_date(qs_dict, months=1)
    elif term == 'half_year':
        graph_data_dict = zero_fill_date(qs_dict, months=6)
    # elif term == 'all':
    #     graph_data_dict = zero_fill(qs_dict, months=6)

    return graph_data_dict

# 辞書をx軸、y軸リストに加工
def dict_to_xy(dict):
    x_data = []
    y_data = []
    
    for key, value in dict.items():
        x_data.append(key)
        y_data.append(value)

    graph_data = {'x':x_data, 'y':y_data}

    print(f'graph_data : {graph_data}')
    

    return graph_data

# term='today'
# クエリごとに累計アルコール摂取量を加算していく
def get_graph_data_today(qs):
    graph_data = {}
    x_data = []
    y_data = []
    sum_alcohol = 0

    # データが空の場合、0をプロットする
    if qs.count() == 0:
        # 10分前に0を追加
        x_data.append(datetime.datetime.now().astimezone(tz.gettz('Asia/Tokyo')) - datetime.timedelta(minutes=10))
        y_data.append(0)

        # 現在時刻に0を追加
        x_data.append(datetime.datetime.now().astimezone(tz.gettz('Asia/Tokyo')))
        y_data.append(0)

    # データが入ってる場合の処理
    else:    
        # グラフの開始点として、一番古いデータの10分前に0をプロット
        x_data.append(qs.earliest('created_at').created_at.astimezone(tz.gettz('Asia/Tokyo')) - datetime.timedelta(minutes=10))
        y_data.append(0)

        # 累計アルコール摂取量を加算していく。
        for q in qs:
            sum_alcohol += q.get_1cup_alcohol_amount()
            x_data.append(q.created_at.astimezone(tz.gettz('Asia/Tokyo')))
            y_data.append(sum_alcohol)
    
    graph_data['x'] = x_data
    graph_data['y'] = y_data

    return graph_data

# term='week', 'month', 'half_year', 'all'
# 日、月ごとにアルコール摂取量を計算する
def get_graph_data(qs, term):
    
    if term == 'today':
        graph_data = get_graph_data_today(qs)

    elif term in ['week', 'month', 'half_year', 'all']:
        # クエリセットを期間に応じて辞書に加工する
        qs_dict = qs_to_dict(qs, term)

        # データの存在しない日、月に0のデータを追加する
        graph_data_dict = zero_fill(qs_dict, term)

        # 辞書をx軸、y軸リストに分割
        graph_data = dict_to_xy(graph_data_dict)

    return graph_data

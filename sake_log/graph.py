import datetime

import io
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import japanize_matplotlib

from .models import AlcoholLogList
from .calc import get_graph_data
from .date import get_start_day

#グラフ作成
def setPlt(request):
    term = request.GET['term']
    qs = AlcoholLogList.objects.filter(user=request.user, created_at__gte=get_start_day(term)).order_by('created_at')
    x = get_graph_data(qs, term)['x']
    y = get_graph_data(qs, term)['y']
    jst = datetime.timezone(datetime.timedelta(hours=9))

    print(f'x = {x}')
    print(f'y = {y}')

    fig = plt.figure(figsize=(5,2.5))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(x, y)

    # 期間に合わせてx軸のメモリを設定する。
    if term == 'today':
        interval = 1
        format = '%H:%M'

        # x軸の日付ラベルを設定
        xfmt = mdates.DateFormatter(format, tz=jst)

        # 間隔を時間に
        xloc = mdates.HourLocator(interval=interval)

    elif term in ['week', 'month', 'half_year', 'all']:
        if term == 'week':
            interval = 1
            format = '%-d'
        elif term == 'month':
            interval = 4
            format = '%-d'
        elif term == 'half_year':
            interval = 30
            format = '%-m/%-d'

        # Formatterでx軸の日付ラベルを月・日に設定
        xfmt = mdates.DateFormatter(format, tz=jst)

        # DayLocatorで間隔を日数に
        xloc = mdates.DayLocator(interval=interval)
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
        
    # 設定したx軸の項目を反映させる
    ax.xaxis.set_major_locator(xloc)
    ax.xaxis.set_major_formatter(xfmt)

    # y軸の最小値を0にする
    ax.set_ylim(0)

    # 軸のフォントサイズ
    x_labels = ax.get_xticklabels()
    y_labels = ax.get_yticklabels()
    plt.setp(x_labels, fontsize=6);
    plt.setp(y_labels, fontsize=6);

    # グラフのタイトル
    plt.title('アルコール摂取量(g)', fontsize=8)

    # プロット！！
    plt.plot(x,y)

    # グリッド線を追加
    plt.grid()

# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


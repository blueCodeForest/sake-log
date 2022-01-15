# graph.py -> グラフの描画に関する処理

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
    
    # 期間に応じて折線グラフと棒グラフを使い分ける
    if term == 'today':
        ax.plot(x, y)
    elif term in ['week', 'month', 'half_year', 'all']:
        ax.bar(x, y)
        
    # データに応じてx軸に適切なメモリを設定する
    xloc = mdates.AutoDateLocator()
    xfmt = mdates.AutoDateFormatter(xloc, tz=jst)
    xfmt.scaled[1/(60 * 24)] = '%H:%M'
    xfmt.scaled[1] = '%-d'
    xfmt.scaled[30] = '%-m月'

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

    # グリッド線を追加
    plt.grid()

# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


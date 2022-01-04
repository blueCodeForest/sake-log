import io
# import seaborn as sns
# sns.set()
import base64

from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import DisplayAlcoholList, DrankAlcoholList, StatusList
from .forms import StatusForm, DrinkForm

# 500エラー原因究明の一時的な処理
# from django.views.decorators.csrf import requires_csrf_token
# from django.http import HttpResponseServerError

# @requires_csrf_token
# def my_customized_server_error(request, template_name='500.html'):
#     import sys
#     from django.views import debug
#     error_html = debug.technical_500_response(request, *sys.exc_info()).content
#     return HttpResponseServerError(error_html)
# ここまで


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'sake_log/index.html'
    model = DisplayAlcoholList
    context_object_name = 'drinks'

    def calc_sum_alcohol_amount(self):
        # 正味アルコール摂取量を合計する
        drinks = DrankAlcoholList.objects.filter(user=self.request.user)
        sum_alcohol_amount = 0
        for drink in drinks:
            sum_alcohol_amount += drink.get_1cup_alcohol_amount()
        sum_alcohol_amount = round(sum_alcohol_amount)
        return sum_alcohol_amount

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum_alcohol_amount'] = self.calc_sum_alcohol_amount()
        status_form = StatusForm()
        context['status_form'] = status_form
        status = StatusList.objects.filter(user=self.request.user).order_by('-created_at').first()
        context['status'] = status

        # ログインユーザーをセッションに追加
        self.request.session['user_name'] = self.request.user.name

        return context
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(user=self.request.user)

        return queryset
        

class DrankAlcoholView(LoginRequiredMixin, ListView):
    template_name = 'sake_log/graph.html'
    model = DrankAlcoholList
    context_object_name = 'drinks'

    # def get_queryset(self):
    #     qs = super().get_queryset().filter(user=self.request.user)
    #     return qs

    # def create_graph(self, x_list, t_list):
    #     plt.cla() # 現在のグラフを消去する
    #     fig = plt.figure(figsize=(10, 7.5), dpi=100, facecolor='w') # 台紙を作成
    #     ax = fig.add_subplot(111, xlabel='yoko', ylabel='tate') # 軸を追加
    #     ax.plot(t_list, x_list, label="x") # 折れ線グラフを追加

    # def get_image(self):
    #     buffer = io.BytesIO()
    #     plt.savefig(buffer, format='png')
    #     image_png = buffer.getvalue()
    #     graph = base64.b64encode(image_png)
    #     graph = graph.decode('utf-8')
    #     buffer.close()
    #     return graph

    # def draw_graph(self):
    #     x_list = [3, 6, 12, 24, 48, 96, 192, 384, 768, 1536]
    #     t_list = [1,2,3,4,5,6,7,8,9,10]
    #     self.create_graph(x_list, t_list)
    #     graph = self.get_image()
    #     return graph

    # def seaborn(self):
    #     df = sns.load_dataset('titanic')
    #     graph = sns.lineplot(x="timepoint", y="signal", data=df, ci=none)
    #     return graph

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # この1行を実行するとエラーになる。なぜ？
        context['graph'] = self.seaborn()

        return context
    

def count_up(request):
    drank_card_id = request.POST.get('drank_card_id')
    user = request.user
    DrankAlcoholList.objects.create(drank_card_id=drank_card_id, user=user)

    return redirect('sake_log:index')


def count_down(request):
    drank_card_id = request.POST.get('drank_card_id')
    user = request.user
    delete_record = DrankAlcoholList.objects.filter(drank_card_id=drank_card_id, user=user).last()
    
    if delete_record:
        delete_record.delete()

    return redirect('sake_log:index')


def change_status(request):
    user = request.user
    status = request.POST.get('status')
    StatusList.objects.create(status=status, user=user)

    return redirect('sake_log:index')


class EditDrink(UpdateView):
    template_name = 'sake_log/edit.html'
    model = DisplayAlcoholList
    context_object_name = 'drink'
    success_url = '/'
    form_class = DrinkForm


class CreateDrink(LoginRequiredMixin, CreateView):
    template_name = 'sake_log/create.html'
    model = DisplayAlcoholList
    success_url = '/'
    form_class = DrinkForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteDrink(DeleteView):
    template_name = 'sake_log/delete.html'
    context_object_name = 'drink'
    model = DisplayAlcoholList
    success_url = '/'


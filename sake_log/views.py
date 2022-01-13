from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q

from .models import DisplayAlcoholList, AlcoholLogList, StatusList
from .forms import StatusForm, DrinkForm
from .date import *
from .calc import *
from .graph import *

# 500エラー原因究明の一時的な処理
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)
# ここまで

# 一覧表示させるビュー
class IndexView(LoginRequiredMixin, ListView):
    template_name = 'sake_log/index.html'
    model = DisplayAlcoholList
    context_object_name = 'drinks'

    def calc_sum_alcohol_amount(self):
        # 正味アルコール摂取量を合計する
        drinks = AlcoholLogList.objects.filter(user=self.request.user, created_at__gte=get_am6_dt())
        sum_alcohol_amount = 0
        for drink in drinks:
            sum_alcohol_amount += drink.get_1cup_alcohol_amount()
        sum_alcohol_amount = round(sum_alcohol_amount)
        return sum_alcohol_amount

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 摂取した総アルコール量
        context['sum_alcohol_amount'] = self.calc_sum_alcohol_amount()

        # 酔い度合い
        status_form = StatusForm()
        context['status_form'] = status_form
        status = StatusList.objects.filter(user=self.request.user).order_by('-created_at').first()
        context['status'] = status

        # ログインユーザーをセッションに追加
        self.request.session['user_name'] = self.request.user.name

        return context
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)

        # 基準時間以降に飲んだ量をcups変数にセット
        queryset = queryset.filter(user=self.request.user).annotate(cups=Count('drank_cards', filter=Q(drank_cards__created_at__gte=get_am6_dt())))

        return queryset

# 履歴を表示するビュー
class AlcoholLogView(LoginRequiredMixin, ListView):
    template_name = 'sake_log/log.html'
    model = AlcoholLogList
    context_object_name = 'drinks'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['term'] = self.kwargs['term']

        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        term = self.kwargs['term']
        queryset = queryset.filter(created_at__gte=get_start_day(term)).order_by('-created_at')

        return queryset

# グラフを描画する
def get_graph(request):
    setPlt(request.GET['term'])  
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response

def count_up(request):
    drank_card_id = request.POST.get('drank_card_id')
    user = request.user
    AlcoholLogList.objects.create(drank_card_id=drank_card_id, user=user)

    return redirect('sake_log:index')


def count_down(request):
    drank_card_id = request.POST.get('drank_card_id')
    user = request.user
    delete_record = AlcoholLogList.objects.filter(drank_card_id=drank_card_id, user=user).last()
    
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


import io
# import seaborn as sns
# sns.set()
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q

from .models import DisplayAlcoholList, DrankAlcoholList, StatusList
from .forms import StatusForm, DrinkForm
from .date import *

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
        drinks = DrankAlcoholList.objects.filter(user=self.request.user, created_at__range=[get_standard_dt(), datetime.now()])
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
        queryset = queryset.filter(user=self.request.user).annotate(cups=Count('drank_cards', filter=Q(drank_cards__created_at__gte=get_standard_dt())))

        return queryset
        

class DrankAlcoholView(LoginRequiredMixin, ListView):
    template_name = 'sake_log/log.html'
    model = DrankAlcoholList
    context_object_name = 'drinks'

    # 履歴の取得範囲を設定
    def get_start_day(self):
        term = self.kwargs['term']
        start_day = datetime.now()

        if term == 'all':
            start_day = DrankAlcoholList.objects.earliest('created_at').created_at
        elif term == 'half_year':
            start_day = get_standard_dt(months=6)
        elif term == 'month':
            start_day = get_standard_dt(months=1)
        elif term == '7days':
            start_day = get_standard_dt(days=7)
        elif term == 'today':
            start_day = get_standard_dt()

        return start_day

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(created_at__range=[self.get_start_day(), datetime.now()])

        return queryset

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


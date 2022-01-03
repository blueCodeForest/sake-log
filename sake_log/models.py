import re
from django.contrib.auth import get_user_model

from django.db import models


class DisplayAlcoholList(models.Model):
    name = models.CharField('名前', max_length=20, blank=False, null=False)
    alcohol_degree = models.IntegerField(
        'アルコール度数',
        blank=False,
        null=False
    )
    AMOUNT_LIST = (
        ("", ""),
        ("大", "大ジョッキ(約500ml)"),
        ("中", "中ジョッキ、チューハイ等(約350ml)"),
        ("小", "小ジョッキ(約200ml)"),
        ("グラス", "グラス(約125ml)"),
        ("ロック", "ロック(約60ml)"),
        ("おちょこ", "おちょこ(約45ml)"),
        ("シングル", "シングル(約30ml)"),
        ("ダブル", "ダブル(約60ml)"),
    )
    amount = models.CharField('サイズ', max_length=50, choices=AMOUNT_LIST)
    memo = models.TextField('メモ', max_length=300, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class DrankAlcoholList(models.Model):
    drank_card = models.ForeignKey(DisplayAlcoholList, on_delete=models.CASCADE, related_name='drank_cards')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def tuple_to_dict(self, tpl):
        new_dict = {}
        for key, value in tpl:
            new_dict[key] = value
        return new_dict

    def get_amount_ml(self):
        # AMOUNT_LISTから容量(ml)を取得
        amount_str = self.tuple_to_dict(DisplayAlcoholList.AMOUNT_LIST)[self.drank_card.amount]
        amount_ml = int(re.sub(r"\D", "", amount_str))
        return amount_ml

    def get_1cup_alcohol_amount(self):
        # 1杯あたりのアルコール量を計算
        return self.get_amount_ml() * self.drank_card.alcohol_degree / 100
    
    def __str__(self):
        return self.drank_card.name
    

class StatusList(models.Model):
    CHOICES = (
        ("0", "素面"),
        ("1", "ほんのり酔ってきた"),
        ("2", "酔っぱらった"),
        ("3", "世界が歪んで見える"),
        ("4", "限界です")
    )

    status = models.CharField(verbose_name='酔っ払い度', max_length=30, choices=CHOICES)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
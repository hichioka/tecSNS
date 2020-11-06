from django import forms
from django.forms import ModelForm


from cms.models import Card, WorkSeat, WSque

import django_filters


#カードフォーム
class CardForm(ModelForm):
# 必須事項じゃなくする
    def __init__(self, *args, **kwd):
        super(CardForm, self).__init__(*args, **kwd)
        self.fields["subtitle"].required = False
        self.fields["desc2"].required = False
        self.fields["desc3"].required = False

    class Meta:
        model = Card
        fields = ('title','subtitle', 'tags', 'tecimg', 'tec_desc', 'desc1','desc2','desc3')


#ワークシートフォーム（webでワークするとき用） queの数は制限するか動的に増やすか
#queの数も科学的に何個がいいみたいなエビデンスあるといい
class WSqueForm(ModelForm):
# 必須事項じゃなくする
    def __init__(self, *args, **kwd):
        super(WSque, self).__init__(*args, **kwd)
        self.fields["question2"].required = False
        self.fields["question3"].required = False
        self.fields["question4"].required = False
        self.fields["question5"].required = False

    class Meta:
        model = WSque
        fields = ('title', 'question1', 'question2', 'question3', )


#ソートフォームテスト
class SortChoice(forms.Form):
  choice1 = forms.fields.ChoiceField(
        choices = (
            ('cre', '追加日順'),
            ('upd', '更新日順'),
            ('aiu', '五十音順'),
            ('tag', 'タグ関連'),
            ('osu', 'おすすめ')
        ),
        required=True,
        widget=forms.widgets.Select
    )



#複数選択可能なチェックボックス　テスト
class ChkForm(forms.Form):
     labels = ['チェック','複数チェック','ラジオボタン','動的選択肢１','動的選択肢２']#ココノイミヨクワカッテナイ

     four = forms.MultipleChoiceField(
          label=labels[3],
          required=False,
          disabled=False,
          widget=forms.CheckboxSelectMultiple(attrs={
               'id': 'four','class': 'form-check-input'}))

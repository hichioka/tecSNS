from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views import View
from django.views import generic

from cms.models import Card
from cms.forms import  CardForm, ChkForm

from django.db.models import Q

from django.views.decorators.http import require_POST



#カード関係の処理
def card_list(request):
    """カードの一覧"""
    cards = Card.objects.all().order_by('id') #全部のidを取得して、cardsに入れている
    return render(request, 'cms/card_list.html',     # 使用するテンプレート
                  {'cards': cards})         # テンプレートに渡すデータList


def card_edit(request, card_id=None):
    """カードの編集"""
    if card_id:   # card_id が指定されている (修正時)
        card = get_object_or_404(Card, pk=card_id)
    else:         # card_id が指定されていない (追加時)
        card = Card()

    if request.method == 'POST':
        card = Card()#格納するためのインスタンスを作成
        form = CardForm(request.POST, request.FILES, instance=card,)  # POST された request データからフォームを作成、描画
        if form.is_valid():    # フォームのバリデーション
            card = form.save(commit=False)
            card.save()
            return redirect('cms:card_list')
    else:    # GET の時
        form = CardForm(instance=card)  # card インスタンスからフォームを作成

    return render(request, 'cms/card_edit.html', dict(form=form, card_id=card_id))


def card_del(request, card_id):
    """カードの削除"""
    # return HttpResponse('カードの削除')
    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return redirect('cms:card_list')


def card_detail(request, card_id):
    """カードの詳細"""
    card = get_object_or_404(Card, pk=card_id)
    return render(request, 'cms/card_detail.html',     # 使用するテンプレートのパス
                  {'card': card})


class CardSearch(ListView):
    """カードの検索"""
    model = Card
    template_name = 'cms/card_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None) #Qはorやandに変換される
        #検索時の条件指定
        lookups = (
            Q(title__icontains=query) |
            Q(subtitle__icontains=query) |
            Q(tec_desc__icontains=query) |
            Q(desc1__icontains=query) |
            Q(desc2__icontains=query) |
            Q(desc3__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct() #distinctで重複を防ぐ
            return qs
        qs = super().get_queryset()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


def card_choice(request):
    """印刷するカードの選択画面に遷移"""

    # チェックボックスから値があるのかないのかで条件分けして表示する
    # 値がないときはchoiceに遷移
    # 値があるときはchoicedに遷移
    if request.method == "POST":
        cardlist = request.POST.getlist('choice')
        cards = Card.objects.get_queryset().filter(id=cardlist[*])

        return render(request, 'cms/card_choiced.html',
                  {'cards': cards})
    else:
        cards = Card.objects.all().order_by('id')
        return render(request, 'cms/card_choice.html',     # 使用するテンプレート
                  {'cards': cards})


# def card_choiced(request, card_id):
#     """カード洗濯画面で、選択の処理"""
#     if request.method == "POST":
#         # cards = Card
#         cardlist = request.POST.getlist('choice')
#         card = get_object_or_404(cardlist,  pk=card_id) #choiceでポストされたidからdbに該当するデータを引き出してきて、それを格納
#         print(card)

#         return render(request, 'cms/card_choiced.html',     # 使用するテンプレート
#                   {'cards': card})


#複数選択テスト
# def card_choice(request):
#     labels = ['チェック','複数チェック','ラジオボタン','動的選択肢１','動的選択肢２']
#     # 入力結果を格納する辞書
#     results = {}
#     radios = {}
#     ret = ''
#     if request.method == 'POST':
#         # 入力されたデータの受取
#         results[labels[0]] = request.POST.getlist("one")
#         results[labels[1]] = request.POST.getlist("two")
#         results[labels[2]] = request.POST.getlist("three")
#         results[labels[3]] = request.POST.getlist("four")
#         results[labels[4]] = request.POST.getlist("five")
#         ret = 'OK'
#         c = {'results': results,'ret':ret}
#     else:    
#         form = forms.ChkForm()
#         choice1 = []
#         choice1.append(('1','動的選択肢１'))
#         choice1.append(('2','動的選択肢２'))
#         choice1.append(('3','動的選択肢３'))
#         choice1.append(('4','動的選択肢４'))
#         form.fields['four'].choices = choice1
#         form.fields['four'].initial = ['2']    
#         form.fields['five'].choices = choice1
#         form.fields['five'].initial = ['3']    
#         c = {'form': form,'ret':ret}
#         # CFRF対策（必須）
#         c.update(csrf(request))
#     return render(request,'demo03.html',c)


# class card_choice(generic.ListView):
#     paginate_by = 5
#     template_name = 'cms/card_choice.html'
#     model = Card
#     def post(self, request, *args, **kwargs):
#         checks_value = request.Card.getlist('checks[]')
#         logger.debug("checks_value = " + str(checks_value))


# #ソートクラス
# class card_search(generic.ListView):
#     model = Card
 
#     def get_queryset(self):
#         # タグフラグがTrueで、作成日順に並び替え
#         card = super().get_queryset().filter(tags=True).order_by('-title')
#         return render(request, 'cms/card_search.html',     # 使用するテンプレートのパス
#                   {'card': card})


# class SampleChoiceView(View):
#     """ソートの中身"""
#     def get(self, request):
#         form = forms.SortChoice()
#         context = {
#             'form': form
#         }

#         return render(request, 'card_choiced.html', context)

# sample_choice_view = SampleChoiceView.as_view()





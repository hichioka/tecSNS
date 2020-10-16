from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views import generic

from cms.models import Card
from cms.forms import  CardForm
# CardFilter
from django.db.models import Q

from django.views.decorators.http import require_POST



#カード関係の処理
def card_list(request):
    """カードの一覧"""
    # return HttpResponse('カードの一覧')
    cards = Card.objects.all().order_by('id')
    return render(request, 'cms/card_list.html',     # 使用するテンプレート
                  {'cards': cards})         # テンプレートに渡すデータ


def card_edit(request, card_id=None):
    """カードの編集"""
    # return HttpResponse('カードの編集')
    if card_id:   # card_id が指定されている (修正時)
        card = get_object_or_404(Card, pk=card_id)
    else:         # card_id が指定されていない (追加時)
        card = Card()

    if request.method == 'POST':
        card = Card()
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
    """カードの削除"""
    # return HttpResponse('カードの削除')
    card = get_object_or_404(Card, pk=card_id)

    return render(request, 'cms/card_detail.html',     # 使用するテンプレートのパス
                  {'card': card})


class card_search(generic.ListView): #ソートクラス
    model = Card
 
    def get_queryset(self):
        # タグフラグがTrueで、作成日順に並び替え
        return super().get_queryset().filter(tags=True).order_by('-title')


class CardSearch(ListView):  #検索クラス
    model = Card
    template_name = 'cms/card_search.html'
    paginate_by = 8 #検索結果の表示数

    def get_queryset(self):
        query = self.request.GET.get('q', None) #Qはorやandに変換される
        lookups = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
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

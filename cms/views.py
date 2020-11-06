from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views import View
from django.views import generic

from django.db.models import Q

from cms.models import Card, WorkSeat
from cms.forms import  CardForm, ChkForm

from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas



#カード関係の処理
def card_list(request):
    """カードの一覧"""
    cards = Card.objects.all().order_by('id') #全部のidを取得して、cardsに入れている
    return render(request, 'cms/card_list.html',     # 使用するテンプレート
                  {'cards': cards})         # テンプレートに渡すデータ辞書


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


# def card_choice(request):
#     cards = Card.objects.all().order_by('id')
#     return render(request, 'cms/card_choice.html',     # 使用するテンプレート
#                   {'cards': cards})


def ChoiceSaveList(cardlist):
    """印刷するカードをもう一個listに保存してコピー返す関数"""
    savecardlist = cardlist
    return savecardlist


# def card_choiced(request):
#     cards = ChoiceSaveList(request)
#     if len(cards) > 0:
#         return render(request, 'cms/card_choiced.html',
#                   {'cards': cards})
#     else:
#         cards = Card.objects.all().order_by('id')
#         return render(request, 'cms/card_choice.html',     # 使用するテンプレート
#                   {'cards': cards})


def card_choice(request):
    if request.method == "POST":
        cardlist = request.POST.getlist('choice')
        ChoiceSaveList(cardlist) #コピーを作成
        queries = [Q(id__iexact=value) for value in cardlist]
        query = queries.pop()
        for item in queries:
            query |= item
        cards = Card.objects.get_queryset().filter(query)

        return render(request, 'cms/card_choiced.html',
                  {'cards': cards})

    #からで送信した時の条件も入れておく、もしくわifの方に入れておく
    else:#初めにレンダリングする時、POstされて値がないときに帰るようにする
        cards = Card.objects.all().order_by('id')
        return render(request, 'cms/card_choice.html',     # 使用するテンプレート
                  {'cards': cards})


#pdfにして出力
class PdfView(View):

    #関数定義
    filename = 'tecCard.pdf'  # 保存時の出力ファイル名
    font_name = 'HeiseiKakuGo-W5'  # フォントの指定
    title = 'tecCard.pdf'

    # def savelist(request):
    #     if request.method == "POST":
    #         cardlist = request.POST.getlist('choice')
    #         queries = [Q(id__iexact=value) for value in cardlist]
    #         query = queries.pop()
    #         for item in queries:
    #             query |= item
    #         cards = Card.objects.get_queryset().filter(query)
    #     return cards


    def get(self, request, *args, **kwargs):
        # pdf用のContent-TypeやContent-Dispositionをセット
        response = HttpResponse(status=200, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{}"'.format(self.filename)
        # 即ダウンロードしたい時は、attachmentをつける(ページ遷移しない)
        # response['Content-Disposition'] = 'attachment; filename="example.pdf"'
        self._create_pdf(response)
        return response


    def _create_pdf(self, response):

        size = landscape(A4)#横向き
        # size = portrait(A4)#縦向き
        #サイズの変更は後々入れていく

        # pdfを描く場所を作成：pdfの原点は左上にする(bottomup=False)
        p = canvas.Canvas(response, pagesize=size, bottomup=False)
        pdfmetrics.registerFont(UnicodeCIDFont(self.font_name))
        p.setTitle(self.title)  #pdfのタイトルを指定

        # フォントとサイズ(9)を指定して、左から20mm・上から18mmの位置に「はろーわーるど」を表示
        p.setFont(self.font_name, 9)
        p.drawString(20*mm, 18*mm, 'ハロー')

        p.showPage()#改ぺーじ
        #２ページ目で裏面は逆から載せないと、裏と表の内容が違うものになってしまう
        p.setFont(self.font_name, 9)
        p.drawString(20*mm, 18*mm, 'はろーわーるど')

        # pdfの書き出し
        p.save()


def workseat_list(request):
    """カードの一覧"""
    Wseat = WorkSeat.objects.all().order_by('id') #全部のidを取得して、cardsに入れている
    return render(request, 'cms/workseat_list.html',     # 使用するテンプレート
                  {'Wseat': Wseat})         # テンプレートに渡すデータList





from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse, reverse_lazy


#クエリ関係
from django.db.models import Q

#カードのモデル関係
from cms.models import Card, WorkSeat
from cms.forms import  CardForm, ChkForm

#PDF関係
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

#google スプレッドシート関係
import gspread
from oauth2client.service_account import ServiceAccountCredentials



#カード関係のview
class CardList(ListView):
    """カードリスト表示"""
    context_object_name = 'card_list'
    model = Card


class CardDetail(DetailView):
    """カードの詳細"""
    model = Card


class CardCreate(CreateView):
    """カードの新規作成"""
    model = Card
    form_class = CardForm

    def get_success_url(self):
        return reverse('cms:card_list')


class CardUpdate(UpdateView):
    """カードの編集"""
    template_name = 'cms/card_update_form.html'
    model = Card
    form_class = CardForm

    def get_success_url(self):
        return reverse('cms:card_detail', kwargs={'pk': self.object.pk})


class CardDelete(DeleteView):
    """カードの削除"""
    template_name = 'cms/card_confirm_delete.html'
    model = Card
    success_url = reverse_lazy('cms:card_list')


class CardSearch(ListView):
    """カードの検索"""
    model = Card
    template_name = 'cms/card_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None) #Qはorやandに変換される
        lookups = (
            Q(title__icontains=query) |
            Q(subtitle__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct() #distinctで重複を防ぐ
            return qs

        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
    #検索キーワードを一時的にcontextに保存するコード,検索結果がない時とかに使えるcontextはありません的な
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context



# class CardChoice(generic.FormView):
#     """カードの選択・確認・PDF・スプレッドに抽出"""

#     def card_choice(request):#カードの選択
#         if request.method == "POST":
#             cardlist = request.POST.getlist('choice')#ローカル変数
#             ChoiceSaveList(cardlist) #コピーを作成
#             queries = [Q(id__iexact=value) for value in cardlist]
#             query = queries.pop()
#             for item in queries:
#                 query |= item
#             cards = Card.objects.get_queryset().filter(query)


#             return render(request, 'cms/card_choiced.html',
#                   {'cards': cards})

#     #からで送信した時の条件も入れておく、もしくわifの方に入れておく
#         else:#初めにレンダリングする時、Postされて値がないときに帰るようにする
#             cards = Card.objects.all().order_by('id')
#             return render(request, 'cms/card_choice.html',     # 使用するテンプレート
#                   {'cards': cards})

    # def card_confilm(self):#選択したカードの確認
    # #postデータの受け取りと表示で、受け取ったデータを並べておく、スプレッドにしまっておく
    #      return render(request, 'cms/card_choice.html',     # 使用するテンプレート
    #               {'cards': cards})
        


def card_choice(request):#カードの選択
        if request.method == "POST":
            cardlist = request.POST.getlist('choice')#ローカル変数
            queries = [Q(id__iexact=value) for value in cardlist]
            query = queries.pop()
            for item in queries:
                query |= item
            cards = Card.objects.get_queryset().filter(query)


            return render(request, 'cms/card_choiced.html',
                  {'cards': cards})

    #からで送信した時の条件も入れておく、もしくわifの方に入れておく
        else:#初めにレンダリングする時、Postされて値がないときに帰るようにする
            cards = Card.objects.all().order_by('id')
            return render(request, 'cms/card_choice.html',     # 使用するテンプレート
                  {'cards': cards})



#pdfにして出力
class PdfView(View):

    #関数定義
    filename = 'tecCard.pdf'  # 保存時の出力ファイル名
    font_name = 'HeiseiKakuGo-W5'  # フォントの指定
    title = 'tecCard.pdf'

    #ここでpostされたデータを再取得したい、もしくわ継続して引き継ぎたいための処理
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





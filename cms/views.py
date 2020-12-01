from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse, reverse_lazy

from django.conf import settings
from django.conf.urls.static import static

from django.core import serializers

import textwrap

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
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
#画像の処理
from PIL import Image, ImageFilter

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



def card_choice(request):
    """#カードの選択"""
    if request.method == "POST":
        cardlist = request.POST.getlist('choice')
        queries = [Q(id__iexact=value) for value in cardlist]
        query = queries.pop()
        for item in queries:
            query |= item
        cards = Card.objects.get_queryset().filter(query)
        return render(request, 'cms/card_confirm_choice.html', {'cards': cards})

    #からで送信した時の条件も入れておく、もしくわifの方に入れておく
    else:#初めにレンダリングする時、Postされて値がないときに帰るようにする
        cards = Card.objects.all().order_by('id')
        return render(request, 'cms/card_choice.html',{'cards': cards})


# class CreateData(View):
#     """カードを選択して、PDFとスプレッドシートに出力する"""

#         if request.method == "POST":
#             cardlist = request.POST.getlist('choice')#ローカル変数
#             queries = [Q(id__iexact=value) for value in cardlist]
#             query = queries.pop()
#             for item in queries:
#                 query |= item
#             cards = Card.objects.get_queryset().filter(query)

#     def choice(request):
#         return render(request, 'cms/card_confirm_choice.html', {'cards': cards})

#     #からで送信した時の条件も入れておく、もしくわifの方に入れておく
#         else:#初めにレンダリングする時、Postされて値がないときに帰るようにする
#             cards = Card.objects.all().order_by('id')
#             return render(request, 'cms/card_choice.html',{'cards': cards})




#pdfにして出力
class PdfCreate(View):

    #関数定義
    filename = 'tecCard.pdf'  # 保存時の出力ファイル名
    font_name = 'HeiseiKakuGo-W5'  # フォントの指定
    title = 'tecCard.pdf'


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
        # pdfを描く場所を作成：pdfの原点は左上にする(bottomup=False)
        p = canvas.Canvas(response, pagesize=size, bottomup=False)

        pdfmetrics.registerFont(UnicodeCIDFont(self.font_name))
        p.setTitle(self.title)  #pdfのタイトルを指定

        #idの値を取得してリストに格納
        # card = Card.objects.values_list('title', flat=True)
        card_title = Card.objects.values_list('title', flat=True)
        card_sub = Card.objects.values_list('subtitle', flat=True)
        card_img = Card.objects.values_list('tecimg', flat=True)#media/が追加されてないから表示できない
        card_desc = Card.objects.values_list('tec_desc', flat=True)#15文字で改行したい

        titledata = [
        [card_title[0], card_title[1], card_title[2], card_title[3], card_title[4]],
        [card_title[5], card_title[6], card_title[7], card_title[8], card_title[9]],
        ]
        subdata = [
        [card_sub[0], card_sub[1], card_sub[2], card_sub[3], card_sub[4]],
        [card_sub[5], card_sub[6], card_sub[7], card_sub[8], card_sub[9]],
        ]
        imgdata = [
        [card_img[0], card_img[1], card_img[2], card_img[3], card_img[4]],
        [card_img[5], card_img[6], card_img[7], card_img[8], card_img[9]],
        ]
        descdata = [
        [card_desc[0], card_desc[1], card_desc[2], card_desc[3], card_desc[4]],
        [card_desc[5], card_desc[6], card_desc[7], card_desc[8], card_desc[9]],
        ]
        # cardimg = ImageReader(card_img[0:])


        titletable = Table(titledata, colWidths=(55*mm), rowHeights=(91*mm))
        titletable.setStyle(TableStyle([
            ('FONT', (0, 0), (4, 4), self.font_name, 12),
            ('VALIGN', (0, 0), (4, 4), 'BOTTOM'),#文字の縦の位置
            ('ALIGN',  (0, 0), (4, 4), 'CENTER'),#文字の横の位置
        ]))
        subtable = Table(subdata, colWidths=(55*mm), rowHeights=(91*mm))
        subtable.setStyle(TableStyle([
            ('FONT', (0, 0), (4, 4), self.font_name, 9),
            ('VALIGN', (0, 0), (4, 4), 'BOTTOM'),#文字の縦の位置
            ('ALIGN',  (0, 0), (4, 4), 'CENTER'),#文字の横の位置
        ]))
        desctable = Table(descdata, colWidths=(55*mm), rowHeights=(91*mm))
        desctable.setStyle(TableStyle([
            ('FONT', (0, 0), (4, 4), self.font_name, 9),
            ('BOX', (0, 0), (4, 4), 0.5, colors.black),
            ('INNERGRID', (0, 0), (4, 4), 0.25, colors.black),
            ('VALIGN', (0, 0), (4, 4), 'TOP'),
            ('ALIGN',  (0, 0), (4, 4), 'CENTER'),
        ]))

        # imgUrl = Image.open('media/images/autodrive_xHfLITj.png')
        # imgurl = imgUrl.rotate(180)

        #動的にファイルの選択を行えるようにする
        p.drawImage('media/images/autodrive_xHfLITj.png', 20, 100, width=150, height=100, mask='auto',preserveAspectRatio=True)
        #テーブルの書き出し位置の指定
        titletable.wrapOn(p, 10*mm, 20*mm)
        titletable.drawOn(p, 10*mm, 20*mm)
        subtable.wrapOn(p, 10*mm, 25*mm)
        subtable.drawOn(p, 10*mm, 25*mm)
        desctable.wrapOn(p, 10*mm, 14*mm)
        desctable.drawOn(p, 10*mm, 14*mm)

        p.showPage()#改ぺーじで２ページ目
        #２ページ目で裏面は逆から載せないと、裏と表の内容が違うものになってしまう
        # imgtable.wrapOn(p, 10*mm, 14*mm)
        # imgtable.drawOn(p, 10*mm, 14*mm)

        # pdfの書き出し
        p.save()



def SpredCreate(request):
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('cms/tech-card-2894e3e99fd6.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('teccard test').sheet1

    #dbから項目ごとに情報を取得
    title = Card.objects.values_list('title', flat=True)
    subt = Card.objects.values_list('subtitle', flat=True)
    imgurl = Card.objects.values_list('tecimg', flat=True)
    tecdesc = Card.objects.values_list('tec_desc', flat=True)
    desc1 = Card.objects.values_list('desc1', flat=True)
    desc2 = Card.objects.values_list('desc2', flat=True)
    desc3 = Card.objects.values_list('desc3', flat=True)
    
    #選択したデータ数の記述
    sinfo = wks.range('A1:C3')
    sinfo[0].value = '選択した技術数'
    sinfo[3].value = 'count'

    #スプレッドシートの項目の書き込み
    sitems = wks.range('A4:G4')
    items = [
    '技術名称','技術サブ名称','イラストURL','技術概要','技術活用事例1','技術活用事例2','技術活用事例3',
    ]
    i = 0
    for sitem in items:
        sitems[i].value = sitem
        i += 1

    #セルの範囲指定
    stitle = wks.range('A5:A30')#終わりの範囲を選択した数にする
    ssub = wks.range('B5:B30')
    simg = wks.range('C5:C30')
    sdesc = wks.range('D5:D30')
    sdsub1 = wks.range('E5:E30')
    sdsub2 = wks.range('F5:F30')
    sdsub3 = wks.range('G5:G30')

    #クエリをlistに保存と
    j = 0
    for st, ss, si, sd, sd1, sd2, sd3 in zip(title, subt, imgurl, tecdesc, desc1, desc2, desc3 ):
        stitle[j].value = st
        ssub[j].value = ss
        simg[j].value = si
        sdesc[j].value = sd
        sdsub1[j].value = sd1
        sdsub2[j].value = sd2
        sdsub3[j].value = sd3
        j += 1

    #スプレッドシートに書き込むlist
    itemlist = [
    sinfo, sitems, stitle, ssub, simg, sdesc, sdsub1, sdsub2, sdsub3
    ]
    for wksitem in itemlist:
        wks.update_cells(wksitem)

    return HttpResponseRedirect('https://docs.google.com/spreadsheets/d/16Z_kNldNcmH0BbXgVKyI8kFah4iJiVBnL5erZ3Dqg18/edit#gid=0')



def workseat_list(request):
    """カードの一覧"""
    Wseat = WorkSeat.objects.all().order_by('id') #全部のidを取得して、cardsに入れている
    return render(request, 'cms/workseat_list.html',     # 使用するテンプレート
                  {'Wseat': Wseat})         # テンプレートに渡すデータList


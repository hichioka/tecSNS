from django.forms import ModelForm

from cms.models import Book, Impression, Card


class BookForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Book
        fields = ('name', 'publisher', 'page', )


class ImpressionForm(ModelForm):
    """感想のフォーム"""
    class Meta:
        model = Impression
        fields = ('comment', )


class CardForm(ModelForm):
# subtitleを必須事項じゃなくする
    def __init__(self, *args, **kwd):
        super(CardForm, self).__init__(*args, **kwd)
        self.fields["subtitle"].required = False
        self.fields["desc2"].required = False
        self.fields["desc3"].required = False

    class Meta:
        model = Card
        fields = ('title','subtitle','tecimg', 'tec_desc', 'desc1','desc2','desc3')
        # widgets = {
        #     'title': ModelForm.Textarea(
        #         attrs={'rows': 1, 'cols': 20, 'placeholder': '技術名称'}
        #     ),
        #     'subtitle': ModelForm.Textarea(
        #         attrs={'rows': 1, 'cols': 20, 'placeholder': 'サブ技術名称'}
        #     ),
        # }

# データベースから該当のデータを持ってきて、編集する機能を入れたい

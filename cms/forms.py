from django.forms import ModelForm

from cms.models import Card

import django_filters



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


# class CardFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(lookup_expr='iexact')

#     class Meta:
#         model = Card
#         fields = ['title', 'tags']


# class CardDetail(ModelForm):
#   """カードの詳細"""
#   class Meta:
#         model = Card
#         fields = ('title','subtitle','tecimg', 'tec_desc', 'desc1','desc2','desc3')

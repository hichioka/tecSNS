from django.urls import path
from cms import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'cms'
urlpatterns = [
    # path(urlの表示名、view名.viewの中の関数名、name=リダイレクトなどで使うときの名前)

    #カード投稿
    path('card/', views.card_list, name='card_list'),   # 一覧
    path('card/add/', views.card_edit, name='card_add'),  # 登録
    path('card/mod/<int:card_id>/', views.card_edit, name='card_mod'),  # 修正
    path('card/del/<int:card_id>/', views.card_del, name='card_del'),   # 削除
    path('card/detail/<int:card_id>', views.card_detail, name='card_detail'),   # 詳細
    path('card/search/', views.CardSearch.as_view(), name='card_search'),   # 検索結果
    path('card/choice/', views.card_choice, name='card_choice'),   # カード選択
    path('card/choiced/', views.card_choice, name='card_choiced'),   # カード選択
    # path('card/print/', views.card_choice, name='card_print'),   # カード選択

    path('workseat/', views.workseat_list, name='workseat_list'),


]  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
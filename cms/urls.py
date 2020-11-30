from django.urls import path
from cms import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'cms'
urlpatterns = [

    #カード投稿
    path('card/', views.CardList.as_view(), name='card_list'),   # 一覧
    path('card/detail/<int:pk>/', views.CardDetail.as_view(), name='card_detail'),   # 詳細
    path('card/create/', views.CardCreate.as_view(), name='card_create'),  # 登録
    path('card/detail/<int:pk>/update', views.CardUpdate.as_view(), name='card_update'),  # 編集
    path('card/detail/<int:pk>/delete', views.CardDelete.as_view(), name='card_del'),   # 削除
    path('card/search/', views.CardSearch.as_view(), name='card_search'),   # 検索結果

    path('card/choice/', views.card_choice, name='card_choice'),   # カード選択
    # path('card/choice/', views.CreateData.as_view(), name='card_choice'),   # カード選択
    # path('card/choiced/', views.PdfCreate.as_view(), name='card_choiced'),   # カード選択

    # path('card/choice/', views.CardChoice.as_view(), name='card_choice'),   # カード選択
    # path('card/choiced/', views.CardChoice.as_view(), name='card_choiced'),   # カード選択


    path('card/print/', views.PdfCreate.as_view(), name='card_print'),   # PDFを表示
    path('card/spredseat/', views.SpredCreate, name='card_spred'),   # スプレッドに書き込み

    #ワークシートのページ
    path('workseat/', views.workseat_list, name='workseat_list'),


]  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
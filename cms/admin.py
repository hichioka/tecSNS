from django.contrib import admin

from cms.models import Book, Impression, Post, WorkSeat

# admin.site.register(Book)
# admin.site.register(Impression)


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'page',)  # 一覧に出したい項目
    list_display_links = ('id', 'name',)  # 修正リンクでクリックできる項目
admin.site.register(Book, BookAdmin)


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment',)
    list_display_links = ('id', 'comment',)
    raw_id_fields = ('book',)   # 外部キーをプルダウンにしない（データ件数が増加時のタイムアウトを予防）
admin.site.register(Impression, ImpressionAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'subtitle',)
    list_display_links = ('id', 'title',)
admin.site.register(Post, PostAdmin)


class WorkSeatAdmin(admin.ModelAdmin):
    list_display = ('id','title',)
    list_display_links = ('id', 'title',)
admin.site.register(WorkSeat, WorkSeatAdmin)
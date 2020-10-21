from django.contrib import admin

from cms.models import Card, WorkSeat, WSque



class CardAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'subtitle', 'tag_list') #adminには画像のURLを取得して乗せたい
    list_display_links = ('id', 'title',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Card, CardAdmin)


class WorkSeatAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'desc',)
    list_display_links = ('id', 'title',)
admin.site.register(WorkSeat, WorkSeatAdmin)


class WSFormAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'question1', 'question2', 'question3', 'question4', 'question5',)
    list_display_links = ('id', 'title',)
admin.site.register(WSque, WSFormAdmin)
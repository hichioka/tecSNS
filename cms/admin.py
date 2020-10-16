from django.contrib import admin

from cms.models import Card, WorkSeat

# admin.site.register(Book)
# admin.site.register(Impression)


class CardAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'subtitle', 'tag_list') #adminには画像のURLを取得して乗せたい
    list_display_links = ('id', 'title',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Card, CardAdmin)


class WorkSeatAdmin(admin.ModelAdmin):
    list_display = ('id','title',)
    list_display_links = ('id', 'title',)
admin.site.register(WorkSeat, WorkSeatAdmin)
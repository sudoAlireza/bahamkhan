from django.contrib import admin

from squads.models import Squad, Membership, Comment
from django_jalali.admin.filters import JDateFieldListFilter


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


class SquadAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]



class CommentAdmin(admin.ModelAdmin):
    def jalali_date(self, obj):
        return obj.pub_date.strftime("%d %b %Y %H:%M")
    jalali_date.admin_order_field = 'pub_date'
    jalali_date.short_description = 'تاریخ ایجاد'
    list_display = ('author', 'body','pub_date' , 'jalali_date',)
    list_filter = (
        ('pub_date', JDateFieldListFilter),
        )
    search_fields = ('body',)


admin.site.register(Squad, SquadAdmin)
admin.site.register(Membership)
admin.site.register(Comment, CommentAdmin)
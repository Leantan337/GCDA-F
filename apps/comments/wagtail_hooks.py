from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import Comment

class CommentAdmin(ModelAdmin):
    model = Comment
    menu_label = 'Comments'
    menu_icon = 'comment'
    menu_order = 300
    list_display = ('author', 'page', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('text', 'author__username')
    list_per_page = 20
    ordering = ['-created_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author', 'page')

modeladmin_register(CommentAdmin)
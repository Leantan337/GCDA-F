from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import NewsCategory

class NewsCategoryAdmin(ModelAdmin):
    model = NewsCategory
    menu_label = 'News Categories'
    menu_icon = 'tag'
    menu_order = 200
    list_display = ('name', 'slug')
    search_fields = ('name',)

modeladmin_register(NewsCategoryAdmin)

from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def getattribute(obj, attr):
    """
    Get an attribute of an object dynamically from a string name
    """
    if hasattr(obj, attr):
        value = getattr(obj, attr)
        if callable(value):
            return value()
        return value
    return ""

@register.filter
def field_heading(field_name, view):
    """
    Return the heading for a specific field for a ModelAdmin view.
    """
    heading = None
    if hasattr(view, 'get_field_headings'):
        headings = view.get_field_headings()
        heading = headings.get(field_name)
    if heading is None:
        heading = field_name.replace('_', ' ').title()
    
    class HeadingObject:
        def __init__(self, text, sortable=False, sort_query_param=None):
            self.text = text
            self.sortable = sortable
            self.sort_query_param = sort_query_param
    
    return HeadingObject(heading)

@register.filter
def get_field_display(obj, field_name):
    """
    Return the display value for a field on an object.
    """
    # First check if the model admin has a get_field_display method
    if hasattr(obj, f'get_{field_name}_display'):
        return getattr(obj, f'get_{field_name}_display')()
    
    # Otherwise try to get the value directly
    if hasattr(obj, field_name):
        value = getattr(obj, field_name)
        # Handle callable
        if callable(value):
            return value()
        return value
    
    return "-"

@register.filter
def admin_urlquote(value):
    """
    Quote a value for use in the admin URLs
    """
    return str(value)

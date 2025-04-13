from wagtail.snippets.models import register_snippet
from .models import NewsCategory

# Register NewsCategory directly as a snippet for simplicity
register_snippet(NewsCategory)

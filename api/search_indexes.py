"""
Декларация индексов Meilisearch модуля (hook discovery).

См. core.search.discovery.load_module_search_indexes и .cursor/rules/search.mdc
"""

from modules.module_template.api.models import TemplateItem


def _template_items_qs():
    return TemplateItem.objects.all()


def _build_template_item_document(item) -> dict:
    return {
        'id': str(item.pk),
        'name': item.name or '',
        'description': item.description or '',
    }


SEARCH_INDEXES = [
    {
        'uid': 'module_template_items',
        'searchable_attributes': ('name', 'description'),
        'get_queryset': _template_items_qs,
        'build_document': _build_template_item_document,
    },
]

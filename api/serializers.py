from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import TemplateItem


class TemplateItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        error_messages={
            'blank': _('Укажите название элемента.'),
            'required': _('Укажите название элемента.'),
        },
    )

    class Meta:
        model = TemplateItem
        fields = ['public_id', 'name', 'description', 'active']
        read_only_fields = ['public_id']

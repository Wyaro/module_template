from rest_framework import serializers

from .models import TemplateItem


class TemplateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateItem
        fields = ['public_id', 'name', 'description', 'active']
        read_only_fields = ['public_id']

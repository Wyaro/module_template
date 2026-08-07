from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from src.core.utils.media_signing import get_signed_media_url_from_field

from .models import TemplateItem


class TemplateItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        error_messages={
            'blank': _('Укажите название элемента.'),
            'required': _('Укажите название элемента.'),
        },
    )
    attachment_url = serializers.SerializerMethodField()
    attachment_name = serializers.SerializerMethodField()
    # write-only: путь из media_api (клиент шлёт attachment_path)
    attachment_path = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = TemplateItem
        fields = [
            'public_id',
            'name',
            'description',
            'active',
            'attachment_url',
            'attachment_name',
            'attachment_path',
        ]
        read_only_fields = ['public_id', 'attachment_url', 'attachment_name']

    def get_attachment_url(self, obj):
        return get_signed_media_url_from_field(obj.attachment)

    def get_attachment_name(self, obj):
        if not obj.attachment or not obj.attachment.name:
            return None
        return obj.attachment.name.replace('\\', '/').rsplit('/', 1)[-1]

    def create(self, validated_data):
        validated_data.pop('attachment_path', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('attachment_path', None)
        return super().update(instance, validated_data)

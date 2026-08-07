from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import connections
from django.utils import timezone
import os
import random
import time

from src.config.version import get_system_version
from src.core.audit.mixin import AuditedModelMixin
from src.core.utils.mixins import MediaApiFileMixin, SwaggerSafeMixin

from .config import MODULE_DATABASE_ALIAS
from .models import TemplateItem
from .permissions import CanViewModuleTemplate
from .serializers import TemplateItemSerializer
from .ml_service import get_model_meta, predict

_service_start = time.monotonic()


class TemplateItemPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


def _demo_metrics() -> dict:
    """Generate demo/stub metrics for the template module health-check."""
    return {
        'latency_ms': round(random.uniform(20, 180), 1),
        'requests_per_minute': round(random.uniform(4, 70), 1),
        'error_rate': round(random.uniform(0, 5.5), 2),
        'uptime_seconds': int(time.monotonic() - _service_start),
        'environment': os.getenv('DJANGO_ENV', 'development'),
        'node_name': os.getenv('NODE_NAME', 'node-1'),
    }


class TemplateItemViewSet(MediaApiFileMixin, AuditedModelMixin, SwaggerSafeMixin, viewsets.ModelViewSet):
    """CRUD TemplateItem + демо media_api (attachment_path / multipart)."""

    serializer_class = TemplateItemSerializer
    pagination_class = TemplateItemPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    audit_module = 'module_template'
    audit_entity_type = 'templateitem'
    audit_action_map = {
        'create': 'module_template.templateitem.created',
        'update': 'module_template.templateitem.updated',
        'destroy': 'module_template.templateitem.deleted',
    }
    permission_classes = [IsAuthenticated, CanViewModuleTemplate]
    lookup_field = 'public_id'
    lookup_url_kwarg = 'public_id'

    def get_queryset(self):
        queryset = TemplateItem.objects.all().order_by('name')
        if self.is_swagger_fake_view():
            return queryset.none()
        user = self.get_safe_user()
        if user is None or not user.is_authenticated:
            return queryset.none()
        active = self.request.query_params.get('active')
        if active is not None:
            queryset = queryset.filter(active=active.lower() == 'true')
        # Канон search.mdc — параметр q (не legacy search).
        search = (self.request.query_params.get('q') or '').strip()
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def _assign_attachment(self, instance) -> None:
        file, file_path = self.get_file_or_path('attachment')
        if not file and not file_path:
            return
        MediaApiFileMixin.assign_file_field(
            instance,
            'attachment',
            file=file,
            file_path=file_path,
        )
        instance.save(update_fields=['attachment'])

    def perform_create(self, serializer):
        instance = serializer.save()
        self._assign_attachment(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._assign_attachment(instance)


class HealthViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, CanViewModuleTemplate]

    @action(detail=False, methods=['get'], url_path='health')
    def health(self, request):
        db_status = 'fail'
        try:
            with connections[MODULE_DATABASE_ALIAS].cursor() as cursor:
                cursor.execute('SELECT 1')
                db_status = 'ok'
        except Exception:
            db_status = 'fail'

        response_data = {
            'status': 'ok' if db_status == 'ok' else 'fail',
            'db': db_status,
            'time': timezone.now().isoformat(),
            'app_version': get_system_version(),
            **_demo_metrics(),
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='model-meta')
    def model_meta(self, request):
        return Response(get_model_meta(), status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='predict')
    def model_predict(self, request):
        return Response(predict(request.data or {}), status=status.HTTP_200_OK)

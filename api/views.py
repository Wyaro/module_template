from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import connections
from django.utils import timezone
import os
import random
import time

from src.config.version import get_system_version
from .config import MODULE_DATABASE_ALIAS
from .models import TemplateItem
from .serializers import TemplateItemSerializer
from .ml_service import get_model_meta, predict

_service_start = time.monotonic()


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


class TemplateItemViewSet(viewsets.ModelViewSet):
    queryset = TemplateItem.objects.all()
    serializer_class = TemplateItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TemplateItem.objects.all()
        active = self.request.query_params.get('active')
        if active is not None:
            queryset = queryset.filter(active=active.lower() == 'true')
        return queryset


class HealthViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

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

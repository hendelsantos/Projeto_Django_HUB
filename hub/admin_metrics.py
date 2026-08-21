from datetime import timedelta

from django.db.models import Count
from django.utils import timezone


def install_admin_access_metrics(admin_site):
    if getattr(admin_site, 'access_metrics_installed', False):
        return

    original_index = admin_site.index
    admin_site.index_template = 'admin/custom_index.html'

    def index_with_metrics(request, extra_context=None):
        from .models import AccessLog

        now = timezone.now()
        today = timezone.localdate()
        last_7_days = now - timedelta(days=7)

        top_paths = (
            AccessLog.objects.values('path')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )
        recent_accesses = AccessLog.objects.select_related('user').order_by('-created_at')[:8]

        metrics_context = {
            'access_metrics': {
                'total': AccessLog.objects.count(),
                'today': AccessLog.objects.filter(created_at__date=today).count(),
                'last_7_days': AccessLog.objects.filter(created_at__gte=last_7_days).count(),
                'logged_users': AccessLog.objects.exclude(user=None).count(),
                'anonymous': AccessLog.objects.filter(user=None).count(),
                'top_paths': top_paths,
                'recent_accesses': recent_accesses,
            }
        }

        if extra_context:
            metrics_context.update(extra_context)

        return original_index(request, extra_context=metrics_context)

    admin_site.index = index_with_metrics
    admin_site.access_metrics_installed = True

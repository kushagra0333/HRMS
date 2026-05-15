from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Serve Single Page Application
index = never_cache(TemplateView.as_view(template_name='index.html'))


@never_cache
def deploy_info(request):
    return JsonResponse(
        {
            'deployment': settings.DEPLOYMENT_METADATA,
            'employee_id_strategy': 'generate_employee_id',
        }
    )

from django.conf import settings


def google_analytics(request):
    return {"GOOGLE_ANALYTICS_MEASUREMENT_ID": settings.GOOGLE_ANALYTICS_MEASUREMENT_ID}

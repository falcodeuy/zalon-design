from django.conf import settings


def google_analytics(request):
    return {"GOOGLE_ANALYTICS_MEASUREMENT_ID": settings.GOOGLE_ANALYTICS_MEASUREMENT_ID}


def django_settings(request):
    print("Context processor executed")
    return {
        "SERVER_NAME": settings.SERVER_NAME,
    }

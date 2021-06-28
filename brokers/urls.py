from django.contrib import admin
from django.conf.urls.static import static,settings
from django.urls import path,re_path
from django.conf.urls import url
from django.urls.conf import include
from django.views.generic import TemplateView
from .yasg_urls import urlpatterns as yasg_url

urlpatterns = [
    path('api/v1/admin-page/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    path('api/v1/auth/',include('djoser.urls')),
    path('api/v1/auth/',include('djoser.urls.jwt')),
    path('api/v1/auth/',include('djoser.social.urls')),
    path('api/v1/',include('accounts.urls')),
    path('api/v1/',include('core.urls')),
    path('api/v1/',include('clients.urls')),
    path('api/v1/broker/',include('payments.urls')),
    path('api/v1/main/',TemplateView.as_view(template_name="accounts/index.html"))

]

# urlpatterns += [re_path('^.*',TemplateView.as_view(template_name='index.html'))]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += yasg_url




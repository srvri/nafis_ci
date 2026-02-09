#NafisClothingIndustry/urls.py
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView,SpectacularRedocView,SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nafis.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('mydesign/', include('mydesign.urls')), # <-- این خط را اضافه کن
    path('api/v1/', include('apis.urls')),
    path("api-auth/", include('rest_framework.urls')),
    path("api/v1/dj-rest-auth/", include('dj_rest_auth.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # افزودن این خط
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # افزودن این خط
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),  # افزودن این خط

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



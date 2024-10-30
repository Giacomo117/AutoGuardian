from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from WebServer import settings
from scripts import script

urlpatterns = [
                  # Include URLs from the WebSite app
                  path('', include('WebSite.urls')),
                  # Include URLs from the REST app under the 'api/' prefix
                  path('api/', include('REST.urls')),
                  # Admin interface URL
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'WebSite.views.custom_404'
# Execute the script function (if needed) after urlpatterns are defined
#script()

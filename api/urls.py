from django.urls import path,include
from api import views


from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi #noqa




schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('orders', views.order_list, name = 'order_list'),
    # path('order/<int:id>/', views.GetOrder, name='order_url'),
    path('applications', views.application_list, name = 'application_list'),
    path('applications/<int:id>', views.application_detail, name = 'application_detail'),
    path('services', views.services_list, name = 'services_list'),
    path('services/<int:id>', views.services_detail, name = 'services_detail'),
    path('services/<int:id>/to_application/<int:application_id>', views.service_to_application, name = 'service_to_application'),
    path('applications/<int:id>/services/<int:service_id>', views.delete_service, name = 'delete_service'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
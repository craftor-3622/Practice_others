from django.contrib import admin
from django.urls import path, include
from contentfetch import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/index/', views.stock_finder, name='stock_finder'),
    path('stock/delete_comment/', views.delete_comment, name='delete_comment'),
    path('stock/', RedirectView.as_view(url='/stock/index/')),
    path('accounts/', include('accounts.urls')),
]

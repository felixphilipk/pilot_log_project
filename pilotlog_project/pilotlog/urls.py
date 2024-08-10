from django.urls import path
from .views import ImportDataView,export_data_view, get_csrf_token

urlpatterns = [
    path('import/', ImportDataView.as_view(), name='import_data'),
    path('export/', export_data_view, name='export_data'),
    path('csrf-token/', get_csrf_token, name='csrf_token')
]

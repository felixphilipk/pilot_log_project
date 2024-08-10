import os
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .importers import import_pilotlog_data
from .exporters import export_pilotlog_to_csv

# Crf exempt should not be used in production environment this has been added for testing


@method_decorator(csrf_exempt, name='dispatch')
class ImportDataView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if file is None:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(upload_dir, 'uploaded_file.json')
        if file_path:
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            import_pilotlog_data(file_path)
            return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "File not uploaded"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def export_data_view(request):
    return export_pilotlog_to_csv()


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'message': 'CSRF token set'})

# middleware.py
import threading
import json
import requests
from django.utils.deprecation import MiddlewareMixin



class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.body_data = request.body

    def process_response(self, request, response):
        if hasattr(request, 'body_data'):
            body_data = request.body_data
        else:
            body_data = b""

        if request.method != 'GET':
            is_file_upload = 'multipart/form-data' in request.content_type
            keys_to_remove = ['profile_picture', 'identity', 'permis']

            if is_file_upload:
                file_paths = {}
                for key, value in request.FILES.items():
                    if key in keys_to_remove:
                        file_paths[key] = value.name

                # Extract string data from request.POST
                string_data = {}
                for key, value in request.POST.items():
                    if key not in request.FILES:
                        string_data[key] = value

                # Remove the specified keys from the string data
                for key in keys_to_remove:
                    string_data.pop(key, None)

                # Convert string data to JSON string
                body_data = json.dumps(string_data)
        
        ip_address = self.get_client_ip(request)
        user_email = request.user.email if request.user.is_authenticated else None
        country, city = self.get_location_from_ip(ip_address)

        log_data = {
            'method': request.method,
            'path': request.get_full_path(),
            'query_params': json.dumps(request.GET.dict()),
            'body': body_data,
            'response_status': response.status_code,
            'response_body': response.content.decode('utf-8'),
            'ip_address': ip_address,
            'country': country,
            'city': city,
            'user_email': user_email,
        }

        # Start a new thread to log the request/response data
        threading.Thread(target=self.log_data, args=(log_data,)).start()
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location_from_ip(self, ip_address):
        if not ip_address:
            return None, None

        try:
            response = requests.get(f'http://ip-api.com/json/{ip_address}')
            data = response.json()
            country = data.get('country')
            city = data.get('city')
            return country, city
        except Exception as e:
            return None, None

    def log_data(self, log_data):
        from api.models import APILog
        APILog.objects.create(
            method=log_data['method'],
            path=log_data['path'],
            query_params=log_data['query_params'],
            body=log_data['body'],
            response_status=log_data['response_status'],
            response_body=log_data['response_body'],
            ip_address=log_data['ip_address'],
            country=log_data['country'],
            city=log_data['city'],
            user_email=log_data['user_email'],
        )

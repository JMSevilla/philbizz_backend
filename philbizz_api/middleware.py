import os
from django.http import JsonResponse
from django.conf import settings

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.expected_api_key = settings.API_KEY

    def __call__(self, request):
        api_key = request.headers.get('x-api-key')
        environment = request.headers.get('X-Environment')

        if not api_key or not environment:
            return JsonResponse(
                {"error": "Missing required headers: x-api-key and X-Environment"},
                status=400
            )

        if api_key != self.expected_api_key:
            return JsonResponse(
                {"error": "Invalid x-api-key"},
                status=403
            )

        if environment.lower() != 'dev':
            return JsonResponse(
                {"error": "Invalid environment. Only 'dev' is allowed."},
                status=403
            )

        return self.get_response(request)
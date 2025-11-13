# predictor/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        protected_urls = [
            '/predictor/predict/'
        ]

        if not request.user.is_authenticated and request.path.startswith('/predictor/predict/'):
            return redirect(reverse('contacts:login'))

        response = self.get_response(request)
        return response

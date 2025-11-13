from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
   
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
      
        protected_urls = [
            '/predictor/predict/'
          
        ]

        if not request.user.is_authenticated and request.path in protected_urls:
            return redirect(reverse('login'))

        response = self.get_response(request)
        return response

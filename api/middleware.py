# api/middleware.py

import logging
from django.http import JsonResponse
from rest_framework import status

logger = logging.getLogger('api.views')

class SecurityMiddleware:
    """
    Middleware personalizado para mejorar la seguridad del formulario de contacto
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si es una petición al formulario de contacto
        if request.path == '/api/contact/':
            # Validaciones de seguridad adicionales
            client_ip = self.get_client_ip(request)
            
            # Verificar headers sospechosos
            suspicious_headers = [
                'X-Forwarded-For',
                'X-Real-IP',
                'X-Cluster-Client-IP',
            ]
            
            # Log de headers para análisis
            for header in suspicious_headers:
                if request.META.get(f'HTTP_{header.upper().replace("-", "_")}'):
                    logger.info(f"Header {header} detectado desde IP: {client_ip}")
            
            # Verificar User-Agent sospechoso
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            suspicious_agents = ['curl', 'wget', 'python-requests', 'bot', 'crawler']
            
            for agent in suspicious_agents:
                if agent.lower() in user_agent.lower():
                    logger.warning(f"User-Agent sospechoso detectado: {user_agent} desde IP: {client_ip}")
                    # Opcional: bloquear automáticamente
                    # return JsonResponse({'error': 'Acceso no autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """
        Obtener la IP real del cliente considerando proxies
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown')
        return ip

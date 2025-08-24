# api/views.py

from rest_framework import generics
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import json
import re
import logging

# Configurar logger
logger = logging.getLogger('api.views')

# Rate limiting personalizado para el formulario de contacto
class ContactFormThrottle(AnonRateThrottle):
    scope = 'contact_form'

# CORRECCIONES AQUÍ:


@api_view(['POST'])
@throttle_classes([ContactFormThrottle])
def contact_form_submit(request):
    # Obtener IP del cliente para logging
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', 
                                request.META.get('REMOTE_ADDR', 'Unknown'))
    
    try:
        data = request.data
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        # Log del intento de envío
        logger.info(f"Intento de contacto desde IP: {client_ip}, Email: {email}")

        # Validación básica
        if not all([name, email, message]):
            logger.warning(f"Campos faltantes desde IP: {client_ip}")
            return Response({'error': 'Todos los campos son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validación de email más robusta
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            logger.warning(f"Email inválido desde IP: {client_ip}, Email: {email}")
            return Response({'error': 'Formato de email inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validación de longitud de campos
        if len(name) > 100:
            logger.warning(f"Nombre demasiado largo desde IP: {client_ip}")
            return Response({'error': 'El nombre es demasiado largo.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(email) > 254:  # RFC 5321 límite estándar
            logger.warning(f"Email demasiado largo desde IP: {client_ip}")
            return Response({'error': 'El email es demasiado largo.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(message) > 5000:
            logger.warning(f"Mensaje demasiado largo desde IP: {client_ip}")
            return Response({'error': 'El mensaje es demasiado largo.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(message) < 10:
            logger.warning(f"Mensaje demasiado corto desde IP: {client_ip}")
            return Response({'error': 'El mensaje es demasiado corto.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validación de contenido sospechoso (básica)
        suspicious_patterns = [
            r'http[s]?://',  # URLs
            r'www\.',        # WWW links
            r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Multiple emails
        ]
        
        combined_text = f"{name} {email} {message}".lower()
        for pattern in suspicious_patterns:
            if len(re.findall(pattern, combined_text)) > 2:  # Permitir hasta 2 ocurrencias
                logger.warning(f"Contenido sospechoso detectado desde IP: {client_ip}")
                return Response({'error': 'El contenido contiene elementos sospechosos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Construir el mensaje de correo
        subject = f'Mensaje de Contacto de {name} ({email})'
        recipient_list = ['brandonmontealegre15@gmail.com'] # Tu correo donde quieres recibir los mensajes

        # Contexto para la plantilla HTML
        context = {
            'name': name,
            'email': email,
            'message': message,
            'client_ip': client_ip,  # Agregar IP al contexto para referencia
        }

        # Renderizar la plantilla HTML
        html_content = render_to_string('email/contact_form_email.html', context)
        text_content = f'Nombre: {name}\nCorreo: {email}\nIP: {client_ip}\nMensaje:\n{message}'

        # Crear el objeto EmailMultiAlternatives
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_list)
        msg.attach_alternative(html_content, "text/html")

        # Enviar el correo
        msg.send(fail_silently=False)

        # Log del envío exitoso
        logger.info(f"Mensaje enviado exitosamente desde IP: {client_ip}, Email: {email}")
        
        return Response({'message': 'Mensaje enviado con éxito!'}, status=status.HTTP_200_OK)

    except Exception as e:
        # Log del error
        logger.error(f"Error al enviar correo desde IP: {client_ip}: {str(e)}")
        return Response({'error': 'Error interno del servidor al enviar el mensaje.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
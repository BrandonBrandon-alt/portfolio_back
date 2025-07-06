# api/views.py

from rest_framework import generics
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# CORRECCIONES AQUÍ:
from .models import Project
from .serializers import ProjectSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

@csrf_exempt # Solo para desarrollo, considera usar CSRF tokens en producción
def contact_form_submit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            # Validación básica
            if not all([name, email, message]):
                return JsonResponse({'error': 'Todos los campos son requeridos.'}, status=400)

            # Construir el mensaje de correo
            subject = f'Mensaje de Contacto de {name} ({email})'
            recipient_list = ['brandonmontealegre15@gmail.com'] # Tu correo donde quieres recibir los mensajes - ¡REEMPLAZA ESTO!

            # Contexto para la plantilla HTML
            context = {
                'name': name,
                'email': email,
                'message': message,
            }

            # Renderizar la plantilla HTML
            html_content = render_to_string('email/contact_form_email.html', context)
            text_content = f'Nombre: {name}\nCorreo: {email}\nMensaje:\n{message}'

            # Crear el objeto EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_list)
            msg.attach_alternative(html_content, "text/html")

            # Enviar el correo
            msg.send(fail_silently=False)

            return JsonResponse({'message': 'Mensaje enviado con éxito!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido.'}, status=400)
        except Exception as e:
            # Log the error for debugging
            print(f"Error al enviar correo: {e}")
            return JsonResponse({'error': 'Error interno del servidor al enviar el mensaje.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
# Sistema de Rate Limiting para Formulario de Contacto

## ¿Qué es Rate Limiting?

El rate limiting es una técnica de seguridad que limita la cantidad de requests que un cliente puede hacer en un período de tiempo específico. En nuestro caso, protege el formulario de contacto contra:

- **Spam automatizado**
- **Ataques de fuerza bruta**
- **Uso excesivo de recursos**
- **Bots maliciosos**

## Configuración Actual

### Límites Establecidos

```python
'DEFAULT_THROTTLE_RATES': {
    'anon': '100/hour',        # 100 requests por hora para usuarios anónimos
    'user': '200/hour',        # 200 requests por hora para usuarios autenticados  
    'contact_form': '5/hour',  # Solo 5 envíos de formulario por hora por IP
}
```

### Validaciones Implementadas

1. **Validación de campos obligatorios**
2. **Validación de formato de email con regex**
3. **Límites de longitud de campos**
4. **Detección de contenido sospechoso (URLs múltiples)**
5. **Logging de seguridad con IP del cliente**

## Características de Seguridad

### Middleware de Seguridad
- Detección de headers sospechosos
- Análisis de User-Agent
- Logging detallado de intentos

### Logging
- Todos los intentos se registran en `contact_form.log`
- Incluye IP del cliente, email y detalles del intento
- Alertas automáticas para contenido sospechoso

### Validaciones de Contenido
- **Nombre**: Solo letras y espacios, máximo 100 caracteres
- **Email**: Formato RFC estándar, máximo 254 caracteres
- **Mensaje**: Mínimo 10 caracteres, máximo 5000 caracteres
- **Contenido sospechoso**: Máximo 2 URLs por mensaje

## Cómo Funciona

1. **Primer nivel**: Django REST Framework throttling por IP
2. **Segundo nivel**: Validaciones de contenido y formato
3. **Tercer nivel**: Middleware de seguridad personalizado
4. **Logging**: Registro completo para análisis posterior

## Respuestas del Sistema

### Éxito (200)
```json
{
    "message": "Mensaje enviado con éxito!"
}
```

### Rate Limit Excedido (429)
```json
{
    "detail": "Request was throttled. Expected available in X seconds."
}
```

### Validación Fallida (400)
```json
{
    "error": "Descripción específica del error"
}
```

## Monitoreo y Análisis

### Archivos de Log
- `contact_form.log`: Registro de todos los intentos
- Console logging para desarrollo

### Métricas Importantes
- Intentos por IP
- Patrones de spam
- Errores de validación
- Intentos exitosos

## Configuración para Producción

### Variables de Entorno Recomendadas
```env
# Rate limiting más estricto para producción
CONTACT_FORM_RATE_LIMIT=3/hour
SUSPICIOUS_CONTENT_THRESHOLD=1
ENABLE_IP_BLOCKING=True
```

### Mejoras Adicionales Sugeridas

1. **Lista negra de IPs**: Bloqueo automático de IPs problemáticas
2. **Integración con reCAPTCHA**: Para validación humana adicional
3. **Análisis de spam más avanzado**: Machine learning para detectar patrones
4. **Notificaciones automáticas**: Alertas por email cuando se detecta spam

## Comandos Útiles

### Verificar logs
```bash
tail -f contact_form.log
```

### Limpiar rate limiting cache (desarrollo)
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

### Análisis de logs
```bash
grep "WARNING" contact_form.log | wc -l  # Contar advertencias
grep "ERROR" contact_form.log            # Ver errores
```

## Pruebas

### Probar rate limiting
```bash
# Enviar múltiples requests rápidamente
for i in {1..10}; do
    curl -X POST http://localhost:8000/api/contact/ \
         -H "Content-Type: application/json" \
         -d '{"name":"Test","email":"test@test.com","message":"Test message"}' &
done
```

### Verificar respuesta de throttling
Después de 5 requests en una hora, deberías recibir un error 429.

## Conclusión

Este sistema de rate limiting proporciona múltiples capas de protección:
- ✅ Previene spam automatizado
- ✅ Protege recursos del servidor
- ✅ Proporciona logging detallado
- ✅ Validaciones robustas de contenido
- ✅ Fácil monitoreo y análisis

El sistema es configurable y puede ajustarse según las necesidades específicas del sitio web.

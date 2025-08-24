#!/usr/bin/env python3
"""
Script de prueba para verificar el rate limiting del formulario de contacto.
Ejecutar después de iniciar el servidor Django.
"""

import requests
import time
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000"  # Cambiar según tu configuración
CONTACT_ENDPOINT = f"{BASE_URL}/api/contact/"

# Datos de prueba
test_data = {
    "name": "Test User",
    "email": "test@example.com",
    "message": "Este es un mensaje de prueba para verificar el rate limiting."
}

def test_rate_limiting():
    """
    Prueba el rate limiting enviando múltiples requests.
    """
    print("🚀 Iniciando pruebas de rate limiting...")
    print(f"Endpoint: {CONTACT_ENDPOINT}")
    print("-" * 50)
    
    success_count = 0
    throttled_count = 0
    error_count = 0
    
    # Enviar 10 requests para probar el límite de 5/hora
    for i in range(1, 11):
        try:
            response = requests.post(
                CONTACT_ENDPOINT,
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"Request {i}: Status {response.status_code}")
            
            if response.status_code == 200:
                success_count += 1
                print(f"  ✅ Éxito: {response.json().get('message', 'OK')}")
            elif response.status_code == 429:
                throttled_count += 1
                print(f"  ⚠️  Rate limited: {response.json()}")
            else:
                error_count += 1
                print(f"  ❌ Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"Request {i}: ❌ Error de conexión: {e}")
        
        # Pequeña pausa entre requests
        time.sleep(0.5)
    
    print("-" * 50)
    print("📊 Resumen de pruebas:")
    print(f"  ✅ Éxitos: {success_count}")
    print(f"  ⚠️  Rate limited: {throttled_count}")
    print(f"  ❌ Errores: {error_count}")
    
    if throttled_count > 0:
        print("\n🎉 ¡Rate limiting funcionando correctamente!")
        print("💡 Los requests fueron limitados después de alcanzar el límite.")
    else:
        print("\n⚠️  Rate limiting no se activó.")
        print("💡 Puede que necesites enviar más requests o verificar la configuración.")

def test_validation():
    """
    Prueba las validaciones de contenido.
    """
    print("\n🔍 Probando validaciones de contenido...")
    print("-" * 50)
    
    test_cases = [
        {
            "name": "Email inválido",
            "data": {
                "name": "Test User",
                "email": "email_invalido",
                "message": "Mensaje de prueba"
            },
            "expected": 400
        },
        {
            "name": "Nombre vacío",
            "data": {
                "name": "",
                "email": "test@example.com",
                "message": "Mensaje de prueba"
            },
            "expected": 400
        },
        {
            "name": "Mensaje muy corto",
            "data": {
                "name": "Test User",
                "email": "test@example.com",
                "message": "Hi"
            },
            "expected": 400
        },
        {
            "name": "Contenido sospechoso",
            "data": {
                "name": "Test User",
                "email": "test@example.com",
                "message": "Visit http://spam.com and http://malware.com and http://phishing.com for more!"
            },
            "expected": 400
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(
                CONTACT_ENDPOINT,
                json=test_case["data"],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == test_case["expected"]:
                print(f"✅ {test_case['name']}: Validación correcta (Status {response.status_code})")
            else:
                print(f"❌ {test_case['name']}: Esperado {test_case['expected']}, obtenido {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {test_case['name']}: Error de conexión: {e}")

if __name__ == "__main__":
    print("🔒 Sistema de Pruebas de Rate Limiting")
    print("=====================================")
    
    # Verificar si el servidor está ejecutándose
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Servidor disponible en {BASE_URL}")
    except requests.exceptions.RequestException:
        print(f"❌ No se puede conectar al servidor en {BASE_URL}")
        print("💡 Asegúrate de que el servidor Django esté ejecutándose:")
        print("   python manage.py runserver")
        exit(1)
    
    # Ejecutar pruebas
    test_validation()
    test_rate_limiting()
    
    print("\n🏁 Pruebas completadas!")
    print("💡 Revisa los logs del servidor para más detalles.")

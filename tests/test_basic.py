"""
tests/test_basic.py

Tests básicos para BookShelf Cloud API.
Validan que la app FastAPI (server/main.py) levanta
y que los endpoints principales responden correctamente.
"""

import pytest
from fastapi.testclient import TestClient

# ─────────────────────────────────────────────────────────
# El main.py está en server/main.py
# Se importa como: from server.main import app
# ─────────────────────────────────────────────────────────
from server.main import app

client = TestClient(app)


# ══════════════════════════════════════════════
# Test 1: Sanity check — la app instancia
# ══════════════════════════════════════════════
def test_app_is_running():
    """
    Verifica que la app FastAPI instancia correctamente.
    Si falla → problema de imports o configuración base.
    """
    assert app is not None


# ══════════════════════════════════════════════
# Test 2: Health check / root endpoint
# ══════════════════════════════════════════════
def test_root_endpoint_no_crash():
    """
    Verifica que el endpoint raíz / responde sin error 5xx.
    No nos importa el status exacto, solo que la app no crashea.
    """
    response = client.get("/")
    assert response.status_code < 500, (
        f"El endpoint / retornó error interno: {response.status_code}. "
        "Revisar logs de la app."
    )


# ══════════════════════════════════════════════
# Test 3: Documentación OpenAPI disponible
# ══════════════════════════════════════════════
def test_openapi_schema_available():
    """
    FastAPI genera /openapi.json automáticamente.
    Si falla → la app tiene un problema de configuración grave.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200, (
        "El schema OpenAPI no está disponible en /openapi.json"
    )
    data = response.json()
    assert "openapi" in data, "La respuesta no tiene el campo 'openapi'"
    assert "paths" in data, "La respuesta no tiene el campo 'paths'"


# ══════════════════════════════════════════════
# Test 4: Endpoint de libros responde algo válido
# ══════════════════════════════════════════════
def test_books_endpoint_responds():
    """
    Verifica que /books responde sin error interno.
    Acepta: 200 (ok), 401 (requiere auth), 404 (no existe aún), 422 (validación).
    NO acepta: 500 (error del servidor).
    """
    response = client.get("/books")
    assert response.status_code in [200, 401, 404, 422], (
        f"El endpoint /books retornó un error inesperado: {response.status_code}"
    )


# ══════════════════════════════════════════════
# Test 5: Crear libro — validación básica
# ══════════════════════════════════════════════
def test_create_book_bad_payload_returns_422():
    """
    Enviar un payload vacío a POST /books debe retornar 422 (Unprocessable Entity).
    FastAPI valida automáticamente los campos requeridos.
    Si retorna 500 → hay un bug en el manejo de errores.
    """
    response = client.post("/books", json={})
    # 422 = validación fallida (esperado)
    # 404 = endpoint no existe aún (aceptable en MVP)
    # 401 = requiere autenticación (aceptable)
    assert response.status_code in [401, 404, 422], (
        f"Se esperaba 422/404/401 con payload vacío, "
        f"pero se obtuvo: {response.status_code}"
    )

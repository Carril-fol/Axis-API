"""Barrido de los 38 endpoints contra un servidor corriendo.

No es un reemplazo de tests/: no hay asserts mas alla del status code y las
llamadas dependen del orden (la 3 usa el token de la 2, la 10 el producto de la
6). Es la red que agarra lo que solo se ve corriendo la API de verdad —
serializacion, validacion de respuesta de spectree, decoradores de permisos—,
que es donde apareceron todos los bugs del 30/08.

Arranca de una base recien migrada y vacia de datos (solo el seed de permisos) y
la deja usada: crea empresa, usuarios, roles, categorias, productos y stock, y
termina con los destructivos.

Cerca del final registra una segunda empresa y le pide los recursos de la
primera: con un solo token, los decoradores `require_*_from_same_company` solo
ejercitan su camino feliz y el 403 no lo prueba nadie. Esas llamadas declaran
`espera=403` y cuentan como OK; el resto sigue esperando 2xx.

    python scripts/sweep.py                        # http://127.0.0.1:8000
    python scripts/sweep.py http://127.0.0.1:8010

Stdlib pura, sin `requests`: no agrega dependencias al proyecto.
"""
import json
import sys
from http.cookiejar import CookieJar
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPCookieProcessor, Request, build_opener

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"

JAR = CookieJar()
opener = build_opener(HTTPCookieProcessor(JAR))
resultados = []
TOKEN = [None]


def call(metodo, ruta, body=None, auth=True, nota="", token=None, espera=None):
    datos = json.dumps(body).encode() if body is not None else None
    # urllib no escapa la ruta (requests si): sin esto, un nombre con espacios
    # como "COCA COLA 2.25" corta el request con InvalidURL.
    req = Request(BASE + quote(ruta, safe="/?&="), data=datos, method=metodo)
    req.add_header("Content-Type", "application/json")
    bearer = token or (TOKEN[0] if auth else None)
    if bearer:
        req.add_header("Authorization", "Bearer " + bearer)

    try:
        with opener.open(req, timeout=20) as r:
            codigo, crudo = r.status, r.read()
    except HTTPError as e:
        codigo, crudo = e.code, e.read()
    except URLError as e:
        print("no hay servidor en %s (%s)" % (BASE, e.reason))
        raise SystemExit(1)

    try:
        cuerpo = json.loads(crudo)
    except Exception:
        cuerpo = {"_raw": crudo[:120].decode(errors="replace")}

    resultados.append((metodo, ruta, codigo, cuerpo, nota, espera))
    return codigo, cuerpo


USER = {"first_name": "folco", "last_name": "carril", "email": "owner@acme.test",
        "password": "secreto123", "confirm_password": "secreto123"}
COMPANY = {"name": "acme", "country": "argentina", "address": "calle falsa 123"}

USER_B = {"first_name": "otra", "last_name": "duenia", "email": "owner@otra.test",
          "password": "secreto123", "confirm_password": "secreto123"}
COMPANY_B = {"name": "otra sa", "country": "argentina", "address": "calle real 456"}

call("GET", "/health", auth=False)
call("POST", "/auth/api/v1/register", {"user": USER, "company": COMPANY}, auth=False)
_, b = call("POST", "/auth/api/v1/login",
            {"email": "owner@acme.test", "password": "secreto123"}, auth=False)
TOKEN[0] = b.get("access_token")
if not TOKEN[0]:
    print("no hubo token, corto:", json.dumps(b)[:200])
    raise SystemExit(1)

# categories
call("POST",  "/categories/api/v1/create", {"name": "bebidas"})
call("GET",   "/categories/api/v1/get/all")
call("GET",   "/categories/api/v1/get/1")
call("GET",   "/categories/api/v1/search/BEBIDAS")
call("PATCH", "/categories/api/v1/update/1", {"name": "bebidas frias"})
# products
call("POST",  "/products/api/v1/create", {"name": "coca cola 2.25", "description": "gaseosa retornable", "category_id": 1, "quantity": 48})
call("GET",   "/products/api/v1/get/all")
call("GET",   "/products/api/v1/get/1")
call("GET",   "/products/api/v1/search/COCA COLA 2.25")
call("PATCH", "/products/api/v1/update/1", {"description": "gaseosa retornable de 2.25 litros"})
# stock
call("GET",   "/stock/api/v1/get/all")
call("GET",   "/stock/api/v1/get/1")
call("GET",   "/stock/api/v1/get/low")
call("PATCH", "/stock/api/v1/update/1", {"quantity": 3})
# roles
call("POST",  "/roles/api/v1/create-role", {"name": "vendedor"})
call("GET",   "/roles/api/v1/get-roles")
call("GET",   "/roles/api/v1/get/2")
call("PATCH", "/roles/api/v1/update/2", {"name": "cajero"})
# role-permissions
call("GET",   "/role-permissions/api/v1/get/1", nota="OWNER, 24 permisos")
call("POST",  "/role-permissions/api/v1/assign-permission-to-role", {"role_id": 2, "permission_id": [1, 2]})
call("GET",   "/role-permissions/api/v1/get/2")
call("PATCH", "/role-permissions/api/v1/update/25", {"role_id": 2, "permission_id": 3}, nota="el <id> es el del link, no el del rol")
call("DELETE", "/role-permissions/api/v1/revoke?role_id=2&permission_id=2")
# users from company
call("POST",  "/users/api/v1/create-user-from-company", {"first_name": "ana", "last_name": "lopez", "email": "ana@acme.test", "password": "secreto123", "confirm_password": "secreto123", "role_id": 2})
call("GET",   "/users/api/v1/get-users-from-company")
call("PATCH", "/users/api/v1/update-user-from-company/2", {"first_name": "anita"})
# companies
call("GET",   "/companies/api/v1/detail/1")
call("PATCH", "/companies/api/v1/update/1", {"address": "avenida siempreviva 742"})
# otra empresa: el 403 de los decoradores de ownership
_, b = call("POST", "/auth/api/v1/register", {"user": USER_B, "company": COMPANY_B},
            auth=False, nota="segunda empresa, no comparte nada con la primera")
OTRO = b.get("access_token")
call("GET",   "/products/api/v1/get/1", auth=False, token=OTRO, espera=403)
call("GET",   "/roles/api/v1/get/2", auth=False, token=OTRO, espera=403)
call("GET",   "/stock/api/v1/get/1", auth=False, token=OTRO, espera=403)
call("PATCH", "/users/api/v1/update-user-from-company/2", {"first_name": "intruso"},
     auth=False, token=OTRO, espera=403)
# destructivos al final
call("PATCH", "/roles/api/v1/assign-role", {"user_id": 2, "role_id": 2})
call("DELETE", "/users/api/v1/delete-user-from-company/2")
call("DELETE", "/roles/api/v1/delete/2")
call("PATCH", "/products/api/v1/deactivate/1")
call("DELETE", "/categories/api/v1/disable/1")
# auth final. La cookie de refresh sale con Secure, asi que ningun cliente
# conforme la manda de vuelta por http: se lee del jar y se pasa por header,
# que la API tambien acepta (JWT_TOKEN_LOCATION incluye "headers").
refresh = next((c.value for c in JAR if c.name == "refresh_token_cookie"), None)
call("POST",  "/auth/api/v1/refresh", auth=False, token=refresh,
     nota="refresh por header: la cookie Secure no viaja por http")
call("POST",  "/auth/api/v1/logout")

print("%-2s %-7s %-52s COD" % ("", "METODO", "RUTA"))
print("-" * 78)
malos = []
for m, ruta, cod, cuerpo, nota, espera in resultados:
    ok = cod == espera if espera else cod < 400
    marca = "  " if ok else ("!!" if cod >= 500 else " ?")
    if not ok:
        malos.append((m, ruta, cod, cuerpo))
    print("%-2s %-7s %-52s %s%s" % (
        marca, m, ruta, cod, "" if espera is None else " (esperado %d)" % espera))

print()
print("%d llamadas | OK: %d | 4xx: %d | 5xx: %d" % (
    len(resultados), len(resultados) - len(malos),
    sum(1 for x in malos if x[2] < 500), sum(1 for x in malos if x[2] >= 500)))
if malos:
    print("\nDETALLE DE LOS QUE NO DIERON LO ESPERADO")
    print("=" * 78)
    for m, ruta, cod, cuerpo in malos:
        print("%s  %s %s" % (cod, m, ruta))
        print("     %s" % json.dumps(cuerpo)[:220])

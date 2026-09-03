"""Vacia los datos de la base dejando el schema y los permisos.

El barrido (`scripts/sweep.py`) asume una base sin datos: empieza registrando la
empresa y da por sentado que la categoria que crea es la id 1, el producto la 1,
el rol nuevo la 2. Correrlo dos veces sin limpiar da 4xx que no son bugs.

No toca `permissions` ni `alembic_version`: los permisos los siembra
`start_server()` al arrancar, y conservarlos evita tener que reiniciar la app
entre barridos (ademas de mantener los ids 1..24 que el barrido usa).

    python scripts/reset_data.py        -> muestra que hay
    python scripts/reset_data.py --si   -> lo vacia
"""
import os
import re
import sys

from sqlalchemy import create_engine, text

TABLAS = ["stock", "role_permission", "users_companies", "products",
          "categories", "roles", "users", "companies"]


def url_de_entorno() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    crudo = open(os.path.join(raiz, ".env"), encoding="utf-8").read()
    return re.search(r'DATABASE_URL\s*=\s*"([^"]+)"', crudo).group(1)


URL = url_de_entorno()
engine = create_engine(URL)
print("destino:", re.sub(r"//[^@]+@", "//", URL.split("?")[0]))

with engine.connect() as c:
    for tabla in TABLAS + ["permissions"]:
        print("   %-18s %6d filas" % (
            tabla, c.execute(text('SELECT count(*) FROM "%s"' % tabla)).scalar()))

if "--si" not in sys.argv:
    print("\nNo se toco nada. Volve a correrlo con --si para vaciar.")
    raise SystemExit(0)

with engine.begin() as c:
    c.execute(text("TRUNCATE %s RESTART IDENTITY CASCADE" % ", ".join(TABLAS)))

with engine.connect() as c:
    quedan = {t: c.execute(text('SELECT count(*) FROM "%s"' % t)).scalar()
              for t in TABLAS + ["permissions"]}
print("\nvaciado. quedan:", {k: v for k, v in quedan.items() if v})
print("ahora: python scripts/sweep.py")

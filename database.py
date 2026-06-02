"""
database.py
-----------
Maneja la base de datos de las canciones.

Funciona con DOS motores automáticamente:
- En tu PC (sin configurar nada): usa SQLite (archivo 'canciones.db').
- En el servidor (Render): si existe la variable de entorno DATABASE_URL
  (la de Neon/Postgres), usa Postgres y los datos quedan guardados de forma
  permanente.

Así, en tu computadora seguís trabajando igual que siempre, y online los
cambios no se pierden.
"""

import os
import sqlite3
from pathlib import Path

# ¿Hay base Postgres configurada? (Render/Neon define DATABASE_URL)
DATABASE_URL = os.environ.get("DATABASE_URL", "")
USAR_POSTGRES = bool(DATABASE_URL)

if USAR_POSTGRES:
    import psycopg2
    import psycopg2.extras

# La base SQLite se guarda en la misma carpeta que este archivo (uso local).
RUTA_DB = Path(__file__).parent / "canciones.db"

# Categorías sugeridas para agrupar las canciones (se pueden agregar otras nuevas).
CATEGORIAS_SUGERIDAS = [
    "Coros clásicos",
    "Clásicas Pop",
    "Contemporáneas",
    "Nuevas y últimas",
]

# Nombre que se usa cuando una canción todavía no tiene categoría asignada.
SIN_CATEGORIA = "Sin categoría"


def conectar():
    """Abre una conexión a la base de datos (Postgres o SQLite)."""
    if USAR_POSTGRES:
        return psycopg2.connect(DATABASE_URL)
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    return conexion


def _placeholders(sql):
    """SQLite usa '?' y Postgres usa '%s'. Convierte según el motor."""
    return sql.replace("?", "%s") if USAR_POSTGRES else sql


def _ejecutar(sql, params=(), fetch=None):
    """Ejecuta una consulta y devuelve resultados según 'fetch'.

    fetch = 'one'  -> una fila
    fetch = 'all'  -> todas las filas
    fetch = 'id'   -> el id recién insertado
    fetch = None   -> nada (INSERT/UPDATE/DELETE simple)
    """
    con = conectar()
    try:
        if USAR_POSTGRES:
            cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cur = con.cursor()
        cur.execute(_placeholders(sql), params)

        resultado = None
        if fetch == "one":
            resultado = cur.fetchone()
        elif fetch == "all":
            resultado = cur.fetchall()
        elif fetch == "id":
            if USAR_POSTGRES:
                fila = cur.fetchone()
                resultado = fila["id"] if fila else None
            else:
                resultado = cur.lastrowid
        con.commit()
        return resultado
    finally:
        con.close()


def inicializar():
    """Crea la tabla de canciones si no existe y agrega columnas faltantes."""
    if USAR_POSTGRES:
        crear = """
            CREATE TABLE IF NOT EXISTS canciones (
                id            SERIAL PRIMARY KEY,
                titulo        TEXT NOT NULL,
                artista       TEXT DEFAULT '',
                tono          TEXT DEFAULT '',
                etiquetas     TEXT DEFAULT '',
                letra         TEXT DEFAULT '',
                categoria     TEXT DEFAULT '',
                youtube       TEXT DEFAULT '',
                creada_en     TEXT DEFAULT (CURRENT_TIMESTAMP::text),
                modificada_en TEXT DEFAULT (CURRENT_TIMESTAMP::text)
            )
        """
    else:
        crear = """
            CREATE TABLE IF NOT EXISTS canciones (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo        TEXT NOT NULL,
                artista       TEXT DEFAULT '',
                tono          TEXT DEFAULT '',
                etiquetas     TEXT DEFAULT '',
                letra         TEXT DEFAULT '',
                categoria     TEXT DEFAULT '',
                youtube       TEXT DEFAULT '',
                creada_en     TEXT DEFAULT CURRENT_TIMESTAMP,
                modificada_en TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
    _ejecutar(crear)

    # Migración para bases viejas (SQLite local que no tenían estas columnas).
    if not USAR_POSTGRES:
        con = conectar()
        try:
            columnas = [f["name"] for f in con.execute("PRAGMA table_info(canciones)")]
            if "categoria" not in columnas:
                con.execute("ALTER TABLE canciones ADD COLUMN categoria TEXT DEFAULT ''")
            if "youtube" not in columnas:
                con.execute("ALTER TABLE canciones ADD COLUMN youtube TEXT DEFAULT ''")
            con.commit()
        finally:
            con.close()


def contar_canciones():
    """Cantidad total de canciones (para saber si hay que cargar datos)."""
    fila = _ejecutar("SELECT COUNT(*) AS n FROM canciones", fetch="one")
    return fila["n"] if fila else 0


def listar_canciones(busqueda=""):
    """Devuelve todas las canciones ordenadas por título.

    Si se pasa 'busqueda', filtra por título, artista, etiquetas, categoría o letra.
    """
    like = "ILIKE" if USAR_POSTGRES else "LIKE"
    orden = "LOWER(titulo)" if USAR_POSTGRES else "titulo COLLATE NOCASE"

    if busqueda:
        patron = f"%{busqueda}%"
        sql = f"""
            SELECT * FROM canciones
            WHERE titulo {like} ? OR artista {like} ? OR etiquetas {like} ?
               OR categoria {like} ? OR letra {like} ?
            ORDER BY {orden}
        """
        return _ejecutar(sql, (patron, patron, patron, patron, patron), fetch="all")

    return _ejecutar(f"SELECT * FROM canciones ORDER BY {orden}", fetch="all")


def agrupar_por_categoria(canciones):
    """Agrupa una lista de canciones por categoría.

    Orden: categorías sugeridas primero, luego otras (alfabético), y al final
    las que no tienen categoría.
    """
    grupos = {}
    for c in canciones:
        cat = (c["categoria"] or "").strip() or SIN_CATEGORIA
        grupos.setdefault(cat, []).append(c)

    orden = []
    for cat in CATEGORIAS_SUGERIDAS:
        if cat in grupos:
            orden.append(cat)
    otras = sorted(
        c for c in grupos
        if c not in CATEGORIAS_SUGERIDAS and c != SIN_CATEGORIA
    )
    orden.extend(otras)
    if SIN_CATEGORIA in grupos:
        orden.append(SIN_CATEGORIA)

    return [(cat, grupos[cat]) for cat in orden]


def obtener_cancion(cancion_id):
    """Devuelve una canción por su id, o None si no existe."""
    return _ejecutar(
        "SELECT * FROM canciones WHERE id = ?", (cancion_id,), fetch="one"
    )


def crear_cancion(titulo, artista, tono, etiquetas, letra, categoria="", youtube=""):
    """Inserta una canción nueva y devuelve su id."""
    sql = """
        INSERT INTO canciones (titulo, artista, tono, etiquetas, letra, categoria, youtube)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    if USAR_POSTGRES:
        sql += " RETURNING id"
    return _ejecutar(sql, (titulo, artista, tono, etiquetas, letra, categoria, youtube), fetch="id")


def actualizar_cancion(cancion_id, titulo, artista, tono, etiquetas, letra,
                       categoria="", youtube=""):
    """Modifica una canción existente."""
    sql = """
        UPDATE canciones
        SET titulo = ?, artista = ?, tono = ?, etiquetas = ?, letra = ?,
            categoria = ?, youtube = ?, modificada_en = CURRENT_TIMESTAMP
        WHERE id = ?
    """
    if USAR_POSTGRES:
        sql = sql.replace("CURRENT_TIMESTAMP", "(CURRENT_TIMESTAMP::text)")
    _ejecutar(sql, (titulo, artista, tono, etiquetas, letra, categoria, youtube, cancion_id))


def borrar_cancion(cancion_id):
    """Elimina una canción de la base de datos."""
    _ejecutar("DELETE FROM canciones WHERE id = ?", (cancion_id,))

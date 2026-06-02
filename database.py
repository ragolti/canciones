"""
database.py
-----------
Maneja toda la conexión con la base de datos SQLite donde se guardan
las canciones. SQLite viene incluido con Python, no hay que instalar nada.

El archivo de la base se llama 'canciones.db' y se crea solo la primera vez.
"""

import sqlite3
from pathlib import Path

# La base de datos se guarda en la misma carpeta que este archivo.
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
    """Abre una conexión a la base de datos.

    row_factory = sqlite3.Row permite acceder a las columnas por nombre,
    por ejemplo cancion["titulo"] en lugar de cancion[0].
    """
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar():
    """Crea la tabla de canciones si todavía no existe.

    Se llama una vez al arrancar la aplicación.
    """
    with conectar() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS canciones (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo       TEXT NOT NULL,
                artista      TEXT DEFAULT '',
                tono         TEXT DEFAULT '',
                etiquetas    TEXT DEFAULT '',
                letra        TEXT DEFAULT '',
                creada_en    TEXT DEFAULT CURRENT_TIMESTAMP,
                modificada_en TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        # Migraciones: agrega columnas nuevas si la base es vieja y no las tiene.
        columnas = [fila["name"] for fila in con.execute("PRAGMA table_info(canciones)")]
        if "categoria" not in columnas:
            con.execute("ALTER TABLE canciones ADD COLUMN categoria TEXT DEFAULT ''")
        if "youtube" not in columnas:
            con.execute("ALTER TABLE canciones ADD COLUMN youtube TEXT DEFAULT ''")


def listar_canciones(busqueda=""):
    """Devuelve todas las canciones, ordenadas por título.

    Si se pasa un texto en 'busqueda', filtra por título, artista o etiquetas.
    """
    with conectar() as con:
        if busqueda:
            patron = f"%{busqueda}%"
            filas = con.execute(
                """
                SELECT * FROM canciones
                WHERE titulo LIKE ? OR artista LIKE ? OR etiquetas LIKE ?
                   OR categoria LIKE ? OR letra LIKE ?
                ORDER BY titulo COLLATE NOCASE
                """,
                (patron, patron, patron, patron, patron),
            ).fetchall()
        else:
            filas = con.execute(
                "SELECT * FROM canciones ORDER BY titulo COLLATE NOCASE"
            ).fetchall()
    return filas


def agrupar_por_categoria(canciones):
    """Recibe una lista de canciones y las devuelve agrupadas por categoría.

    Devuelve una lista de pares (categoria, [canciones]) ordenada así:
    primero las categorías sugeridas (en su orden), después cualquier otra
    categoría nueva (alfabética), y al final las que no tienen categoría.
    """
    grupos = {}
    for c in canciones:
        cat = (c["categoria"] or "").strip() or SIN_CATEGORIA
        grupos.setdefault(cat, []).append(c)

    orden = []
    # 1) Categorías sugeridas, en el orden definido.
    for cat in CATEGORIAS_SUGERIDAS:
        if cat in grupos:
            orden.append(cat)
    # 2) Otras categorías nuevas (que el usuario haya inventado), alfabéticas.
    otras = sorted(
        c for c in grupos
        if c not in CATEGORIAS_SUGERIDAS and c != SIN_CATEGORIA
    )
    orden.extend(otras)
    # 3) Las sin categoría, al final.
    if SIN_CATEGORIA in grupos:
        orden.append(SIN_CATEGORIA)

    return [(cat, grupos[cat]) for cat in orden]


def obtener_cancion(cancion_id):
    """Devuelve una sola canción por su id, o None si no existe."""
    with conectar() as con:
        return con.execute(
            "SELECT * FROM canciones WHERE id = ?", (cancion_id,)
        ).fetchone()


def crear_cancion(titulo, artista, tono, etiquetas, letra, categoria="", youtube=""):
    """Inserta una canción nueva y devuelve su id."""
    with conectar() as con:
        cursor = con.execute(
            """
            INSERT INTO canciones (titulo, artista, tono, etiquetas, letra, categoria, youtube)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (titulo, artista, tono, etiquetas, letra, categoria, youtube),
        )
        return cursor.lastrowid


def actualizar_cancion(cancion_id, titulo, artista, tono, etiquetas, letra,
                       categoria="", youtube=""):
    """Modifica una canción existente."""
    with conectar() as con:
        con.execute(
            """
            UPDATE canciones
            SET titulo = ?, artista = ?, tono = ?, etiquetas = ?, letra = ?,
                categoria = ?, youtube = ?, modificada_en = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (titulo, artista, tono, etiquetas, letra, categoria, youtube, cancion_id),
        )


def borrar_cancion(cancion_id):
    """Elimina una canción de la base de datos."""
    with conectar() as con:
        con.execute("DELETE FROM canciones WHERE id = ?", (cancion_id,))

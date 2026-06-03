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

# ----- Clasificación de canciones (varias dimensiones) -----
# Estilo / época (es el campo 'categoria', se usa para agrupar en la lista).
CATEGORIAS_SUGERIDAS = ["Coros", "Clásicas", "Contemporáneas", "Nuevas"]
# Función / momento.
FUNCIONES = ["Alabanza", "Adoración"]
# Tempo.
TEMPOS = ["Rápida", "Media", "Lenta"]
# Campos que se pueden cambiar con los botones rápidos (lista blanca de seguridad).
CAMPOS_CLASIFICACION = {"categoria", "funcion", "tempo"}

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

    # Migraciones de columnas nuevas.
    if USAR_POSTGRES:
        _ejecutar("ALTER TABLE canciones ADD COLUMN IF NOT EXISTS categoria TEXT DEFAULT ''")
        _ejecutar("ALTER TABLE canciones ADD COLUMN IF NOT EXISTS youtube TEXT DEFAULT ''")
        _ejecutar("ALTER TABLE canciones ADD COLUMN IF NOT EXISTS estado TEXT DEFAULT 'aprobada'")
        _ejecutar("ALTER TABLE canciones ADD COLUMN IF NOT EXISTS funcion TEXT DEFAULT ''")
        _ejecutar("ALTER TABLE canciones ADD COLUMN IF NOT EXISTS tempo TEXT DEFAULT ''")
    else:
        con = conectar()
        try:
            columnas = [f["name"] for f in con.execute("PRAGMA table_info(canciones)")]
            for col, defecto in [("categoria", "''"), ("youtube", "''"),
                                 ("estado", "'aprobada'"), ("funcion", "''"), ("tempo", "''")]:
                if col not in columnas:
                    con.execute(f"ALTER TABLE canciones ADD COLUMN {col} TEXT DEFAULT {defecto}")
            con.commit()
        finally:
            con.close()

    # Unifica nombres de estilo viejos a los nuevos (idempotente).
    _ejecutar("UPDATE canciones SET categoria='Nuevas' WHERE categoria='Nuevas y últimas'")
    _ejecutar("UPDATE canciones SET categoria='Coros' WHERE categoria='Coros clásicos'")
    _ejecutar("UPDATE canciones SET categoria='Clásicas' WHERE categoria='Clásicas Pop'")

    # Tabla de usuarios (registro / login / roles).
    if USAR_POSTGRES:
        crear_usuarios = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id         SERIAL PRIMARY KEY,
                usuario    TEXT UNIQUE NOT NULL,
                email      TEXT DEFAULT '',
                clave_hash TEXT NOT NULL,
                rol        TEXT DEFAULT 'colaborador',
                creado_en  TEXT DEFAULT (CURRENT_TIMESTAMP::text)
            )
        """
    else:
        crear_usuarios = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario    TEXT UNIQUE NOT NULL,
                email      TEXT DEFAULT '',
                clave_hash TEXT NOT NULL,
                rol        TEXT DEFAULT 'colaborador',
                creado_en  TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
    _ejecutar(crear_usuarios)

    # Tabla de listas guardadas (historial de repertorios de eventos).
    if USAR_POSTGRES:
        crear_listas = """
            CREATE TABLE IF NOT EXISTS listas (
                id             SERIAL PRIMARY KEY,
                nombre         TEXT DEFAULT '',
                usuario        TEXT DEFAULT '',
                usuario_id     INTEGER,
                favorita       INTEGER DEFAULT 0,
                canciones_json TEXT DEFAULT '[]',
                creada_en      TEXT DEFAULT (CURRENT_TIMESTAMP::text)
            )
        """
    else:
        crear_listas = """
            CREATE TABLE IF NOT EXISTS listas (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre         TEXT DEFAULT '',
                usuario        TEXT DEFAULT '',
                usuario_id     INTEGER,
                favorita       INTEGER DEFAULT 0,
                canciones_json TEXT DEFAULT '[]',
                creada_en      TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
    _ejecutar(crear_listas)

    # Quita títulos duplicados (por si una carga anterior quedó a medias)
    # y crea un índice único por título para que no se repitan nunca más.
    if USAR_POSTGRES:
        _ejecutar(
            "DELETE FROM canciones a USING canciones b "
            "WHERE a.id > b.id AND a.titulo = b.titulo"
        )
    else:
        _ejecutar(
            "DELETE FROM canciones WHERE id NOT IN "
            "(SELECT MIN(id) FROM canciones GROUP BY titulo)"
        )
    _ejecutar("CREATE UNIQUE INDEX IF NOT EXISTS ux_canciones_titulo ON canciones (titulo)")


def crear_varias(filas):
    """Inserta muchas canciones en UNA sola conexión (rápido y eficiente).

    Cada fila: (titulo, artista, tono, etiquetas, letra, categoria, youtube).
    Si el título ya existe, la saltea (no duplica). Ideal para la carga inicial.
    """
    con = conectar()
    try:
        cur = con.cursor()
        if USAR_POSTGRES:
            sql = (
                "INSERT INTO canciones "
                "(titulo, artista, tono, etiquetas, letra, categoria, youtube) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (titulo) DO NOTHING"
            )
        else:
            sql = (
                "INSERT OR IGNORE INTO canciones "
                "(titulo, artista, tono, etiquetas, letra, categoria, youtube) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
            )
        cur.executemany(sql, filas)
        con.commit()
    finally:
        con.close()


def contar_canciones():
    """Cantidad total de canciones (para saber si hay que cargar datos)."""
    fila = _ejecutar("SELECT COUNT(*) AS n FROM canciones", fetch="one")
    return fila["n"] if fila else 0


def listar_canciones(busqueda="", solo_aprobadas=True):
    """Devuelve canciones ordenadas por título.

    Si 'solo_aprobadas' es True, muestra únicamente las aprobadas (vista pública).
    Si se pasa 'busqueda', filtra por título, artista, etiquetas, categoría o letra.
    """
    like = "ILIKE" if USAR_POSTGRES else "LIKE"
    orden = "LOWER(titulo)" if USAR_POSTGRES else "titulo COLLATE NOCASE"

    condiciones = []
    params = []
    if solo_aprobadas:
        condiciones.append("(estado = 'aprobada' OR estado IS NULL)")
    if busqueda:
        patron = f"%{busqueda}%"
        condiciones.append(
            f"(titulo {like} ? OR artista {like} ? OR etiquetas {like} ? "
            f"OR categoria {like} ? OR letra {like} ?)"
        )
        params += [patron, patron, patron, patron, patron]

    where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""
    sql = f"SELECT * FROM canciones {where} ORDER BY {orden}"
    return _ejecutar(sql, tuple(params), fetch="all")


def listar_pendientes():
    """Canciones que esperan aprobación (para el panel del administrador)."""
    orden = "creada_en DESC"
    return _ejecutar(
        f"SELECT * FROM canciones WHERE estado = 'pendiente' ORDER BY {orden}",
        fetch="all",
    )


def contar_pendientes():
    """Cuántas canciones están esperando aprobación."""
    fila = _ejecutar(
        "SELECT COUNT(*) AS n FROM canciones WHERE estado = 'pendiente'", fetch="one"
    )
    return fila["n"] if fila else 0


def cambiar_estado(cancion_id, estado):
    """Cambia el estado de una canción (aprobada / pendiente)."""
    _ejecutar("UPDATE canciones SET estado = ? WHERE id = ?", (estado, cancion_id))


def clasificar(cancion_id, campo, valor):
    """Cambia una clasificación (categoria / funcion / tempo) con los botones rápidos.

    'campo' se valida contra una lista blanca para que sea seguro.
    """
    if campo not in CAMPOS_CLASIFICACION:
        return False
    _ejecutar(f"UPDATE canciones SET {campo} = ? WHERE id = ?", (valor, cancion_id))
    return True


# ---------- Usuarios ----------

def contar_usuarios():
    fila = _ejecutar("SELECT COUNT(*) AS n FROM usuarios", fetch="one")
    return fila["n"] if fila else 0


def crear_usuario(usuario, email, clave_hash, rol="colaborador"):
    """Crea un usuario y devuelve su id."""
    sql = "INSERT INTO usuarios (usuario, email, clave_hash, rol) VALUES (?, ?, ?, ?)"
    if USAR_POSTGRES:
        sql += " RETURNING id"
    return _ejecutar(sql, (usuario, email, clave_hash, rol), fetch="id")


def obtener_usuario(usuario):
    """Devuelve un usuario por su nombre, o None."""
    return _ejecutar(
        "SELECT * FROM usuarios WHERE usuario = ?", (usuario,), fetch="one"
    )


# ---------- Listas guardadas (historial de eventos) ----------

def crear_lista(nombre, usuario, usuario_id, canciones_json):
    """Guarda una lista de evento y devuelve su id."""
    sql = """
        INSERT INTO listas (nombre, usuario, usuario_id, canciones_json)
        VALUES (?, ?, ?, ?)
    """
    if USAR_POSTGRES:
        sql += " RETURNING id"
    return _ejecutar(sql, (nombre, usuario, usuario_id, canciones_json), fetch="id")


def listar_listas(usuario=None, solo_favoritas=False):
    """Lista las listas guardadas. Filtra por usuario y/o favoritas."""
    cond = []
    params = []
    if usuario:
        cond.append("usuario = ?")
        params.append(usuario)
    if solo_favoritas:
        cond.append("favorita = 1")
    where = ("WHERE " + " AND ".join(cond)) if cond else ""
    sql = f"SELECT * FROM listas {where} ORDER BY favorita DESC, creada_en DESC"
    return _ejecutar(sql, tuple(params), fetch="all")


def obtener_lista(lista_id):
    return _ejecutar("SELECT * FROM listas WHERE id = ?", (lista_id,), fetch="one")


def cambiar_favorita(lista_id, valor):
    _ejecutar("UPDATE listas SET favorita = ? WHERE id = ?", (1 if valor else 0, lista_id))


def borrar_lista(lista_id):
    _ejecutar("DELETE FROM listas WHERE id = ?", (lista_id,))


def usuarios_de_listas():
    """Nombres de usuario que tienen listas guardadas (para el filtro)."""
    filas = _ejecutar(
        "SELECT DISTINCT usuario FROM listas WHERE usuario <> '' ORDER BY usuario",
        fetch="all",
    )
    return [f["usuario"] for f in filas] if filas else []


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


def crear_cancion(titulo, artista, tono, etiquetas, letra, categoria="", youtube="",
                  estado="aprobada"):
    """Inserta una canción nueva y devuelve su id."""
    sql = """
        INSERT INTO canciones (titulo, artista, tono, etiquetas, letra, categoria, youtube, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    if USAR_POSTGRES:
        sql += " RETURNING id"
    return _ejecutar(
        sql, (titulo, artista, tono, etiquetas, letra, categoria, youtube, estado),
        fetch="id",
    )


def actualizar_cancion(cancion_id, titulo, artista, tono, etiquetas, letra,
                       categoria="", youtube="", estado=None):
    """Modifica una canción existente. Si 'estado' es None, no lo cambia."""
    sets = ["titulo = ?", "artista = ?", "tono = ?", "etiquetas = ?", "letra = ?",
            "categoria = ?", "youtube = ?", "modificada_en = CURRENT_TIMESTAMP"]
    params = [titulo, artista, tono, etiquetas, letra, categoria, youtube]
    if estado is not None:
        sets.append("estado = ?")
        params.append(estado)
    params.append(cancion_id)

    sql = f"UPDATE canciones SET {', '.join(sets)} WHERE id = ?"
    if USAR_POSTGRES:
        sql = sql.replace("CURRENT_TIMESTAMP", "(CURRENT_TIMESTAMP::text)")
    _ejecutar(sql, tuple(params))


def borrar_cancion(cancion_id):
    """Elimina una canción de la base de datos."""
    _ejecutar("DELETE FROM canciones WHERE id = ?", (cancion_id,))

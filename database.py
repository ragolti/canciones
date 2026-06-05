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
import json
import sqlite3
import unicodedata
from pathlib import Path


def sin_acentos(texto):
    """Devuelve el texto en minúsculas y sin acentos (para buscar igual con o sin tilde)."""
    if not texto:
        return ""
    normal = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in normal if unicodedata.category(c) != "Mn").lower()

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
        _ejecutar("ALTER TABLE canciones ADD COLUMN IF NOT EXISTS anio TEXT DEFAULT ''")
    else:
        con = conectar()
        try:
            columnas = [f["name"] for f in con.execute("PRAGMA table_info(canciones)")]
            for col, defecto in [("categoria", "''"), ("youtube", "''"),
                                 ("estado", "'aprobada'"), ("funcion", "''"),
                                 ("tempo", "''"), ("anio", "''")]:
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

    # Tabla de "canciones conocidas" por usuario.
    # Cada fila significa: "el usuario X ya tocó / conoce la canción Y".
    # Así cada usuario puede filtrar y ver solo las que conoce, aunque la base
    # tenga miles de canciones.
    if USAR_POSTGRES:
        crear_conocidas = """
            CREATE TABLE IF NOT EXISTS conocidas (
                usuario_id INTEGER NOT NULL,
                cancion_id INTEGER NOT NULL,
                creada_en  TEXT DEFAULT (CURRENT_TIMESTAMP::text),
                PRIMARY KEY (usuario_id, cancion_id)
            )
        """
    else:
        crear_conocidas = """
            CREATE TABLE IF NOT EXISTS conocidas (
                usuario_id INTEGER NOT NULL,
                cancion_id INTEGER NOT NULL,
                creada_en  TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (usuario_id, cancion_id)
            )
        """
    _ejecutar(crear_conocidas)

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

    Si 'solo_aprobadas' es True, muestra solo las aprobadas (vista pública; las
    ocultas y pendientes no aparecen).
    La búsqueda funciona con o sin acentos (insensible a tildes y mayúsculas).
    """
    orden = "LOWER(titulo)" if USAR_POSTGRES else "titulo COLLATE NOCASE"
    where = "WHERE (estado = 'aprobada' OR estado IS NULL)" if solo_aprobadas else ""
    filas = _ejecutar(f"SELECT * FROM canciones {where} ORDER BY {orden}", fetch="all") or []

    if busqueda:
        q = sin_acentos(busqueda)
        def coincide(f):
            campos = " ".join(str(f[k] or "") for k in
                              ("titulo", "artista", "etiquetas", "categoria", "letra"))
            return q in sin_acentos(campos)
        filas = [f for f in filas if coincide(f)]

    return filas


def contar_apariciones(cancion_id):
    """Cuántas listas guardadas (eventos) incluyen esta canción."""
    filas = _ejecutar("SELECT canciones_json FROM listas", fetch="all") or []
    n = 0
    for f in filas:
        try:
            for c in json.loads(f["canciones_json"] or "[]"):
                if int(c.get("id", -1)) == cancion_id:
                    n += 1
                    break
        except Exception:
            pass
    return n


def fechas_apariciones(cancion_id):
    """Lista de (nombre, creada_en) de los eventos donde apareció la canción."""
    filas = _ejecutar(
        "SELECT nombre, creada_en, canciones_json FROM listas ORDER BY creada_en DESC",
        fetch="all",
    ) or []
    resultado = []
    for f in filas:
        try:
            if any(int(c.get("id", -1)) == cancion_id
                   for c in json.loads(f["canciones_json"] or "[]")):
                resultado.append((f["nombre"], f["creada_en"]))
        except Exception:
            pass
    return resultado


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


def enriquecer(cancion_id, artista=None, anio=None, links=None):
    """Completa datos de una canción (artista/autor, año) y agrega links de YouTube."""
    sets = []
    params = []
    if artista is not None and artista != "":
        sets.append("artista = ?")
        params.append(artista)
    if anio is not None and anio != "":
        sets.append("anio = ?")
        params.append(anio)
    if sets:
        params.append(cancion_id)
        _ejecutar(f"UPDATE canciones SET {', '.join(sets)} WHERE id = ?", tuple(params))
    total_links = None
    if links:
        for l in links:
            if l:
                total_links = agregar_youtube(cancion_id, l)
    return total_links


def agregar_youtube(cancion_id, link):
    """Agrega un link de YouTube a una canción (sin duplicar). Devuelve el total."""
    c = obtener_cancion(cancion_id)
    if not c:
        return 0
    actuales = [l.strip() for l in (c["youtube"] or "").splitlines() if l.strip()]
    if link and link not in actuales:
        actuales.append(link)
    nuevo = "\n".join(actuales)
    _ejecutar("UPDATE canciones SET youtube = ? WHERE id = ?", (nuevo, cancion_id))
    return len(actuales)


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


def listar_usuarios():
    """Devuelve todos los usuarios (id, usuario, rol). Para administración."""
    return _ejecutar(
        "SELECT id, usuario, rol FROM usuarios ORDER BY usuario", fetch="all"
    ) or []


# ---------- Canciones "conocidas" (marcadas por cada usuario) ----------

def es_conocida(usuario_id, cancion_id):
    """¿El usuario marcó esta canción como conocida?"""
    fila = _ejecutar(
        "SELECT 1 AS x FROM conocidas WHERE usuario_id = ? AND cancion_id = ?",
        (usuario_id, cancion_id), fetch="one",
    )
    return bool(fila)


def marcar_conocida(usuario_id, cancion_id):
    """Marca una canción como conocida por el usuario (sin duplicar)."""
    if USAR_POSTGRES:
        _ejecutar(
            "INSERT INTO conocidas (usuario_id, cancion_id) VALUES (?, ?) "
            "ON CONFLICT (usuario_id, cancion_id) DO NOTHING",
            (usuario_id, cancion_id),
        )
    else:
        _ejecutar(
            "INSERT OR IGNORE INTO conocidas (usuario_id, cancion_id) VALUES (?, ?)",
            (usuario_id, cancion_id),
        )


def desmarcar_conocida(usuario_id, cancion_id):
    """Quita la marca de conocida."""
    _ejecutar(
        "DELETE FROM conocidas WHERE usuario_id = ? AND cancion_id = ?",
        (usuario_id, cancion_id),
    )


def alternar_conocida(usuario_id, cancion_id):
    """Marca o desmarca según el estado actual. Devuelve True si quedó conocida."""
    if es_conocida(usuario_id, cancion_id):
        desmarcar_conocida(usuario_id, cancion_id)
        return False
    marcar_conocida(usuario_id, cancion_id)
    return True


def ids_conocidas(usuario_id):
    """Conjunto con los ids de las canciones que el usuario marcó como conocidas."""
    filas = _ejecutar(
        "SELECT cancion_id FROM conocidas WHERE usuario_id = ?",
        (usuario_id,), fetch="all",
    ) or []
    return {f["cancion_id"] for f in filas}


def contar_conocidas(usuario_id):
    """Cuántas canciones tiene marcadas como conocidas el usuario."""
    fila = _ejecutar(
        "SELECT COUNT(*) AS n FROM conocidas WHERE usuario_id = ?",
        (usuario_id,), fetch="one",
    )
    return fila["n"] if fila else 0


def marcar_todas_conocidas(usuario_id, ids):
    """Marca muchas canciones como conocidas para el usuario, en una sola conexión."""
    ids = [int(i) for i in ids]
    if not ids:
        return 0
    con = conectar()
    try:
        cur = con.cursor()
        if USAR_POSTGRES:
            sql = ("INSERT INTO conocidas (usuario_id, cancion_id) VALUES (%s, %s) "
                   "ON CONFLICT (usuario_id, cancion_id) DO NOTHING")
        else:
            sql = "INSERT OR IGNORE INTO conocidas (usuario_id, cancion_id) VALUES (?, ?)"
        cur.executemany(sql, [(usuario_id, i) for i in ids])
        con.commit()
    finally:
        con.close()
    return contar_conocidas(usuario_id)


def quitar_todas_conocidas(usuario_id):
    """Borra todas las marcas de conocidas del usuario."""
    _ejecutar("DELETE FROM conocidas WHERE usuario_id = ?", (usuario_id,))


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


def sugerencias(usuario, estilo=None, limite=10):
    """Sugiere canciones poco/nada usadas según las listas del usuario.

    Prioriza las que NUNCA aparecieron en las listas del usuario; luego las que
    hace más tiempo que no se cantan. Se puede filtrar por estilo (categoria).
    """
    # Canciones candidatas (aprobadas, opcionalmente de un estilo).
    canciones = listar_canciones(solo_aprobadas=True)
    if estilo:
        canciones = [c for c in canciones if (c["categoria"] or "") == estilo]

    # Última vez que el usuario usó cada canción (según sus listas).
    listas = _ejecutar(
        "SELECT canciones_json, creada_en FROM listas WHERE usuario = ?",
        (usuario,), fetch="all",
    ) or []
    ultima_vez = {}
    for l in listas:
        fecha = l["creada_en"] or ""
        try:
            for c in json.loads(l["canciones_json"] or "[]"):
                cid = int(c.get("id", -1))
                if cid not in ultima_vez or fecha > ultima_vez[cid]:
                    ultima_vez[cid] = fecha
        except Exception:
            pass

    # Orden: primero las nunca usadas; luego las más antiguas.
    def clave(c):
        f = ultima_vez.get(c["id"])
        return (f is not None, f or "")
    candidatas = sorted(canciones, key=clave)
    return candidatas[:limite]


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
                       categoria="", youtube="", estado=None, anio=None):
    """Modifica una canción existente. Si 'estado'/'anio' son None, no los cambia."""
    sets = ["titulo = ?", "artista = ?", "tono = ?", "etiquetas = ?", "letra = ?",
            "categoria = ?", "youtube = ?", "modificada_en = CURRENT_TIMESTAMP"]
    params = [titulo, artista, tono, etiquetas, letra, categoria, youtube]
    if estado is not None:
        sets.append("estado = ?")
        params.append(estado)
    if anio is not None:
        sets.append("anio = ?")
        params.append(anio)
    params.append(cancion_id)

    sql = f"UPDATE canciones SET {', '.join(sets)} WHERE id = ?"
    if USAR_POSTGRES:
        sql = sql.replace("CURRENT_TIMESTAMP", "(CURRENT_TIMESTAMP::text)")
    _ejecutar(sql, tuple(params))


def borrar_cancion(cancion_id):
    """Elimina una canción de la base de datos (y sus marcas de 'conocida')."""
    _ejecutar("DELETE FROM conocidas WHERE cancion_id = ?", (cancion_id,))
    _ejecutar("DELETE FROM canciones WHERE id = ?", (cancion_id,))

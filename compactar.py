"""
compactar.py — Detecta y compacta secciones repetidas en letras de canciones.

Problema: letras importadas de cifraclub u otros sitios repiten el estribillo
completo varias veces. Este módulo los detecta y reemplaza las repeticiones
por una sola etiqueta como '(Estribillo)' o '(Coro)'.

Uso desde Python:
    from compactar import compactar_letra, analizar_todas
"""

import re

# ── Acordes ──────────────────────────────────────────────────────────────────
RE_ACORDE = re.compile(
    r'^[A-G][#b]?(?:m|[Mm]aj|[Mm]in|[Dd]im|[Aa]ug|[Ss]us|[Aa]dd|°|º|\+|\d)*'
    r'(?:/[A-G][#b]?(?:m)?)?$'
)
SEPARADORES = {'-', '–', '—', '|', '//', '////'}

# ── Palabras que identifican secciones ───────────────────────────────────────
PALABRAS_SECCION = {
    'estribillo', 'coro', 'intro', 'introducción', 'introduccion',
    'puente', 'bridge', 'parte', 'pre', 'pre-estribillo', 'precoro',
    'solo', 'final', 'bis', 'tag', 'verso', 'estrofa', 'refrán', 'refran',
    'primera', 'segunda', 'tercera', 'cuarta', 'repetir',
}

# ── Ruido importado de sitios de acordes ─────────────────────────────────────
# Líneas que contienen metadata de la descarga y no son letra real.
RE_RUIDO = re.compile(
    r'^(Title:|URL Source:|Markdown Content:|http[s]?://|www\.)',
    re.IGNORECASE
)


def _es_linea_acorde(linea: str) -> bool:
    """True si la línea contiene solo acordes y separadores."""
    tokens = linea.strip().split()
    if not tokens:
        return False
    return all(RE_ACORDE.match(t) or t in SEPARADORES for t in tokens)


def _es_etiqueta_seccion(linea: str) -> bool:
    """True si la línea completa es una etiqueta de sección."""
    s = linea.strip()
    if s.startswith('(') and s.endswith(')'):
        contenido = s[1:-1].lower()
        return any(p in contenido for p in PALABRAS_SECCION)
    return False


def _extraer_etiqueta(linea: str):
    """
    Extrae la etiqueta de sección de una línea, si tiene.
    '(Estribillo)'            → '(Estribillo)'
    'Donde solas (Estribillo)'→ '(Estribillo)'
    'Llena mi habitación'     → None
    """
    s = linea.strip()
    # Línea completa = etiqueta
    if s.startswith('(') and s.endswith(')') and s.count('(') == 1:
        contenido = s[1:-1].lower()
        if any(p in contenido for p in PALABRAS_SECCION):
            return s
    # Etiqueta al final de la línea: "Texto (Nombre)"
    m = re.search(r'\(([^)]+)\)\s*$', s)
    if m:
        contenido = m.group(1).lower()
        if any(p in contenido for p in PALABRAS_SECCION):
            return f'({m.group(1)})'
    return None


def _clave_bloque(lineas: list) -> str:
    """
    Genera una clave del contenido del bloque, ignorando:
    - líneas de acordes
    - etiquetas de sección
    - líneas de ruido (importadas de webs)
    La clave es insensible a mayúsculas/acentos menores.
    """
    partes = []
    for l in lineas:
        s = l.strip()
        if not s:
            continue
        if _es_linea_acorde(s):
            continue
        if _es_etiqueta_seccion(s):
            continue
        if RE_RUIDO.match(s):
            continue
        # Normalizar: minúsculas, quitar puntuación extra
        norm = re.sub(r'[^\w\s]', '', s.lower()).strip()
        if norm:
            partes.append(norm)
    return '\n'.join(partes)


def _etiqueta_de_bloque(lineas: list):
    """Devuelve la mejor etiqueta de sección del bloque, o None."""
    for linea in lineas:
        e = _extraer_etiqueta(linea)
        if e:
            return e
    return None


def limpiar_ruido_importacion(texto: str) -> str:
    """
    Elimina líneas de metadata/ruido que quedan al importar letras de sitios
    de acordes (cifraclub, etc.).
    Ej: 'Title: ...', 'URL Source: ...', 'Markdown Content:'
    """
    if not texto:
        return texto
    lineas_limpias = []
    for l in texto.splitlines():
        s = l.strip()
        # Saltar líneas de ruido
        if RE_RUIDO.match(s):
            continue
        # Saltar líneas sueltas que son solo ':' o '.' (artefactos del markdown)
        if s in (':', '.', '::', '---', '==='):
            continue
        lineas_limpias.append(l)
    # Eliminar líneas en blanco duplicadas al inicio/final
    resultado = '\n'.join(lineas_limpias).strip()
    # Comprimir 3+ líneas en blanco consecutivas a 2
    resultado = re.sub(r'\n{3,}', '\n\n', resultado)
    return resultado


def compactar_letra(texto: str) -> tuple:
    """
    Detecta secciones repetidas y las reemplaza por su etiqueta.

    Retorna (texto_compactado, n_secciones_comprimidas).

    Algoritmo:
    1. Divide en bloques (separados por líneas en blanco).
    2. Para cada bloque calcula una 'clave' basada en las líneas de letra
       (ignora acordes y etiquetas).
    3. Al primer bloque con una clave nueva: lo muestra completo y guarda su etiqueta.
    4. Al mismo bloque repetido: solo deja la etiqueta (ej: '(Estribillo)').
    """
    if not texto or not texto.strip():
        return texto, 0

    # Primero limpiar ruido de importación
    texto = limpiar_ruido_importacion(texto)

    # Dividir en bloques
    bloques_raw = re.split(r'\n{2,}', texto.strip())

    bloques_resultado = []
    vistos = {}          # clave → etiqueta del primer bloque
    n_comprimidos = 0

    for bloque_raw in bloques_raw:
        lineas = bloque_raw.split('\n')
        clave = _clave_bloque(lineas)

        # Bloques sin contenido de letra real (solo acordes/etiquetas):
        # no comprimir, pero incluir en el resultado.
        if len(clave) < 12:
            bloques_resultado.append(bloque_raw)
            continue

        etiqueta_local = _etiqueta_de_bloque(lineas)

        if clave in vistos:
            # Sección ya vista → reemplazar por etiqueta
            etiqueta_referencia = etiqueta_local or vistos[clave] or '(Repetir)'
            bloques_resultado.append(etiqueta_referencia)
            n_comprimidos += 1
        else:
            # Primera vez que vemos este contenido → guardar y mostrar completo
            vistos[clave] = etiqueta_local
            bloques_resultado.append(bloque_raw)

    texto_final = '\n\n'.join(bloques_resultado)
    # Limpiar espacios finales por línea
    texto_final = '\n'.join(l.rstrip() for l in texto_final.splitlines())

    cambio = (texto_final != texto)
    return texto_final, n_comprimidos if cambio else 0


def analizar_todas(canciones: list) -> list:
    """
    Recibe la lista de canciones (dicts con 'id', 'titulo', 'artista', 'letra').
    Devuelve solo las que tendrían cambios, con la propuesta incluida.

    Cada elemento del resultado:
    {
        'id':          int,
        'titulo':      str,
        'artista':     str,
        'letra_orig':  str,
        'letra_nueva': str,
        'n_comprimidos': int,
        'ahorro':      int,   # caracteres eliminados
    }
    """
    propuestas = []
    for c in canciones:
        letra = c.get('letra') or ''
        if not letra.strip():
            continue
        nueva, n = compactar_letra(letra)
        if n > 0 or nueva != letra:
            propuestas.append({
                'id':            c['id'],
                'titulo':        c.get('titulo', ''),
                'artista':       c.get('artista', ''),
                'letra_orig':    letra,
                'letra_nueva':   nueva,
                'n_comprimidos': n,
                'ahorro':        len(letra) - len(nueva),
            })
    return propuestas
